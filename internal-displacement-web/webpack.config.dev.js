var autoprefixer      = require('autoprefixer');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var path              = require('path');
var webpack           = require('webpack');

module.exports = {
  devtool: 'eval',
  entry: [
    // Include WebpackDevServer client. It connects to WebpackDevServer via
    // sockets and waits for recompile notifications. When WebpackDevServer
    // recompiles, it sends a message to the client by socket. If only CSS
    // was changed, the app reload just the CSS. Otherwise, it will refresh.
    // The "?/" bit at the end tells the client to look for the socket at
    // the root path, i.e. /sockjs-node/. Otherwise visiting a client-side
    // route like /todos/42 would make it wrongly request /todos/42/sockjs-node.
    // The socket server is a part of WebpackDevServer which we are using.
    // The /sockjs-node/ path I'm referring to is hardcoded in WebpackDevServer.
    require.resolve('webpack-dev-server/client') + '?/',
    // Include Webpack hot module replacement runtime. Webpack is pretty
    // low-level so we need to put all the pieces together. The runtime listens
    // to the events received by the client above, and applies updates (such as
    // new CSS) to the running application.
    require.resolve('webpack/hot/dev-server'),
    // We ship a few polyfills by default.
    // require.resolve('./polyfills'),
    // Finally, this is your app's code:
    path.join(__dirname, 'src', 'index')
    // We include the app code last so that if there is a runtime error during
    // initialization, it doesn't blow up the WebpackDevServer client, and
    // changing JS code would still trigger a refresh.
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  resolve: {
    extensions: ['', '.js', '.jsx', '.json'],
    alias: {
      config: path.join(__dirname, 'src', 'config', 'development')
    }
  },
  plugins: [
    // Generates an `index.html` file with the <script> injected.
    new HtmlWebpackPlugin({
      inject: true,
      template: path.join(__dirname, 'index.html'),
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  module: {
    loaders: [
      {
        test: /\.js$/,
        loaders: ['babel'],
        include: path.join(__dirname, 'src')
      },
      {
        test: /\.css$/,
        include: path.join(__dirname, 'node_modules'),
        loader: 'style-loader!css-loader!postcss-loader'
      },
      {
        test:   /\.css$/,
        include: path.join(__dirname, 'src'),
        loader: 'style-loader!css-loader?modules&localIdentName=[name]__[local]___[hash:base64:5]&importLoaders=1!postcss-loader'
      },
      {
        test: /\.json$/,
        include: [
          path.join(__dirname, 'src'),
          path.join(__dirname, 'node_modules')
        ],
        loader: 'json'
      },
      {
        test: /\.(ico|jpg|png|gif|eot|otf|svg|ttf|woff|woff2)(\?.*)?$/,
        include: [
          path.join(__dirname, 'src'),
          path.join(__dirname, 'node_modules')
        ],
        exclude: /\/favicon.ico$/,
        loader: 'file',
        query: {
          name: 'static/[name].[hash:8].[ext]'
        }
      },
      // A special case for favicon.ico to place it into build root directory.
      {
        test: /\/favicon.ico$/,
        include: [path.join(__dirname, 'src')],
        loader: 'file',
        query: {
         name: 'favicon.ico?[hash:8]'
        }
      },
      // "html" loader is used to process template page (index.html) to resolve
      // resources linked with <link href="./relative/path"> HTML tags.
      {
        test: /\.html$/,
        loader: 'html',
        query: {
          attrs: ['link:href'],
        }
      }
    ]
  },
  // We use PostCSS for autoprefixing only.
  postcss: function() {
    return [
      autoprefixer({
        browsers: [
          '>1%',
          'last 4 versions',
          'Firefox ESR',
          'not ie < 9', // React doesn't support IE8 anyway
        ]
      }),
    ];
  }
};
