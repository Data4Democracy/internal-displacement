process.env.NODE_ENV = 'development'

var chalk              = require('chalk')
var historyApiFallback = require('connect-history-api-fallback')
var path               = require('path')
var webpack            = require('webpack')
var WebpackDevServer   = require('webpack-dev-server')
var config             = require('../webpack.config.dev')

var compiler
var DEFAULT_PORT             = process.env.PORT || 80
var friendlySyntaxErrorLabel = 'Syntax error:'

console.log(chalk.yellow('INIT'))


function isLikelyASyntaxError(message) {
  return message.indexOf(friendlySyntaxErrorLabel) !== -1
}

function formatMessage(message) {
  return message
    // Make some common errors shorter:
    .replace(
      // Babel syntax error
      'Module build failed: SyntaxError:',
      friendlySyntaxErrorLabel
    )
    .replace(
      // Webpack file not found error
      /Module not found: Error: Cannot resolve 'file' or 'directory'/,
      'Module not found:'
    )
    // Internal stacks are generally useless so we strip them
    .replace(/^\s*at\s.*:\d+:\d+[\s\)]*\n/gm, '') // at ... ...:x:y
    // Webpack loader names obscure CSS filenames
    .replace('./~/css-loader!./~/postcss-loader!', '')
}

function clearConsole() {
  // This seems to work best on Windows and other systems.
  // The intention is to clear the output so you can focus on most recent build.
  process.stdout.write('\x1bc')
}


function addMiddleware(devServer) {
  devServer.use(historyApiFallback({
    // Allow paths with dots in them to be loaded, reference issue #387
    disableDotRule: true,
    // For single page apps, we generally want to fallback to /index.html.
    // However we also want to respect `proxy` for API calls.
    // So if `proxy` is specified, we need to decide which fallback to use.
    // We use a heuristic: if request `accept`s text/html, we pick /index.html.
    // Modern browsers include text/html into `accept` header when navigating.
    // However API calls like `fetch()` won’t generally won’t accept text/html.
    // If this heuristic doesn’t work well for you, don’t use `proxy`.
    htmlAcceptHeaders: ['text/html', '*/*']
  }))

  // Finally, by now we have certainly resolved the URL.
  // It may be /index.html, so let the dev server try serving it again.
  devServer.use(devServer.middleware)
}

function setupCompiler(port) {
  console.log(chalk.yellow('setupCompiler'))

  // "Compiler" is a low-level interface to Webpack.
  // It lets us listen to some events and provide our own custom messages.
  compiler = webpack(config)

  // "invalid" event fires when you have changed a file, and Webpack is
  // recompiling a bundle. WebpackDevServer takes care to pause serving the
  // bundle, so if you refresh, it'll wait instead of serving the old one.
  // "invalid" is short for "bundle invalidated", it doesn't imply any errors.
  compiler.plugin('invalid', function() {
    clearConsole()
    console.log('Compiling...')
  })


  // "done" event fires when Webpack has finished recompiling the bundle.
  // Whether or not you have warnings or errors, you will get this event.
  compiler.plugin('done', function(stats) {
    clearConsole()
    var hasErrors = stats.hasErrors()
    var hasWarnings = stats.hasWarnings()
    if (!hasErrors && !hasWarnings) {
      console.log(chalk.green('Compiled successfully!'))
      console.log()
      console.log('The app is running at:')
      console.log()
      console.log('  ' + chalk.cyan('http://localhost:' + port + '/'))
      console.log()
      console.log('Note that the development build is not optimized.')
      console.log('To create a production build, use ' + chalk.cyan('npm run build') + '.')
      console.log()
      return
    }

    // We have switched off the default Webpack output in WebpackDevServer
    // options so we are going to "massage" the warnings and errors and present
    // them in a readable focused way.
    // We use stats.toJson({}, true) to make output more compact and readable:
    // https://github.com/facebookincubator/create-react-app/issues/401#issuecomment-238291901
    var json = stats.toJson({}, true)
    var formattedErrors = json.errors.map(message =>
      'Error in ' + formatMessage(message)
    )
    var formattedWarnings = json.warnings.map(message =>
      'Warning in ' + formatMessage(message)
    )
    if (hasErrors) {
      console.log(chalk.red('Failed to compile.'))
      console.log()
      if (formattedErrors.some(isLikelyASyntaxError)) {
        // If there are any syntax errors, show just them.
        // This prevents a confusing ESLint parsing error
        // preceding a much more useful Babel syntax error.
        formattedErrors = formattedErrors.filter(isLikelyASyntaxError)
      }
      formattedErrors.forEach(message => {
        console.log(message)
        console.log()
      })
      // If errors exist, ignore warnings.
      return
    }
    if (hasWarnings) {
      console.log(chalk.yellow('Compiled with warnings.'))
      console.log()
      formattedWarnings.forEach(message => {
        console.log(message)
        console.log()
      })
      // Teach some ESLint tricks.
      console.log('You may use special comments to disable some warnings.')
      console.log('Use ' + chalk.yellow('// eslint-disable-next-line') + ' to ignore the next line.')
      console.log('Use ' + chalk.yellow('/* eslint-disable */') + ' to ignore all warnings in a file.')
    }
  })
}

function runDevServer(port) {
  var devServer = new WebpackDevServer(compiler, {
    // Enable hot reloading server. It will provide /sockjs-node/ endpoint
    // for the WebpackDevServer client so it can learn when the files were
    // updated. The WebpackDevServer client is included as an entry point
    // in the Webpack development configuration. Note that only changes
    // to CSS are currently hot reloaded. JS changes will refresh the browser.
    hot: true,
    // It is important to tell WebpackDevServer to use the same "root" path
    // as we specified in the config. In development, we always serve from /.
    publicPath: config.output.publicPath,
    // WebpackDevServer is noisy by default so we emit custom message instead
    // by listening to the compiler events with `compiler.plugin` calls above.
    quiet: true,
    // Reportedly, this avoids CPU overload on some systems.
    // https://github.com/facebookincubator/create-react-app/issues/293
    watchOptions: {
      ignored: /node_modules/
    }
  })


  // Our custom middleware proxies requests to /index.html or a remote API.
  addMiddleware(devServer)

  // Launch WebpackDevServer.
  devServer.listen(port, (err) => {
    if (err) return console.log(err)

    clearConsole()

    console.log(chalk.cyan('Starting the development server...'))
    console.log()
  })
}


function run(DEFAULT_PORT) {
  console.log(chalk.yellow('RUN ON PORT', DEFAULT_PORT))
  setupCompiler(DEFAULT_PORT)
  runDevServer(DEFAULT_PORT)
}

run(DEFAULT_PORT)
