var path         = require('path');
var webpack      = require('webpack');
var autoprefixer = require('autoprefixer');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var PKG_VERSION = require('./package.json').version

// Assert this just to be safe.
// Development builds of React are slow and not intended for production.
if (process.env.NODE_ENV !== "production") {
  throw new Error('Production builds must have NODE_ENV=production.');
}

module.exports = {
  devtool: 'cheap-module-source-map',
  entry: [
    './src/index'
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  output: {
    // The build folder.
    path: path.join(__dirname, 'dist'),
    // Generated JS file names (with nested folders).
    // There will be one main bundle, and one file per asynchronous chunk.
    // We don't currently advertise code splitting but Webpack supports it.
    filename: 'js/[name].js',
    chunkFilename: 'js/[name].[chunkhash:8].chunk.js',
    // We inferred the "public path" (such as / or /my-project) from homepage.
    publicPath: process.env.CDN + '/v' + PKG_VERSION
  },
  resolve: {
    extensions: ['', '.js', '.jsx', '.json'],
    alias: {
      config: path.join(__dirname, 'src', 'config', 'production')
    }
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
    // Generates an `index.html` file with the <script> injected.
    new HtmlWebpackPlugin({
      inject: true,
      template: path.join(__dirname, 'index.html'),
      minify: {
        removeComments: true,
        collapseWhitespace: true,
        removeRedundantAttributes: true,
        useShortDoctype: true,
        removeEmptyAttributes: true,
        removeStyleLinkTypeAttributes: true,
        keepClosingSlash: true,
        minifyJS: true,
        minifyCSS: true,
        minifyURLs: true
      }
    }),
    // This helps ensure the builds are consistent if source hasn't changed:
    new webpack.optimize.OccurrenceOrderPlugin(),
    // Try to dedupe duplicated modules, if any:
    new webpack.optimize.DedupePlugin(),
    // Minify the code.
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        screw_ie8: true, // React doesn't support IE8
        warnings: false
      },
      mangle: {
        screw_ie8: true
      },
      output: {
        comments: false,
        screw_ie8: true
      }
    }),
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
        loader: 'style-loader!css-loader?modules&localIdentName=[name]__[local]___[hash:base64:5]&importLoaders=1!postcss-loader',
        include: path.join(__dirname, 'src')
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
        exclude: /\/favicon.ico$/,
        include: [
          path.join(__dirname, 'src'),
          path.join(__dirname, 'node_modules')
        ],
        loader: 'file',
        query: {
          name: '/files/[name].[ext]'
        }
      },
      // A special case for favicon.ico to place it into build root directory.
      {
        test: /\/favicon.ico$/,
        include: [ path.join(__dirname, 'src') ],
        loader: 'file',
        query: {
          name: '/favicon.ico'
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
