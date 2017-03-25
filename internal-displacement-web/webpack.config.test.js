var autoprefixer = require('autoprefixer');
var path         = require('path');
var webpack      = require('webpack');

module.exports = {
  devtool: 'cheap-module-eval-source-map',
  entry: [
    './src/index'
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  node: {
    fs: "empty"
  },
  plugins: [
    new webpack.IgnorePlugin(/^(buffertools)$/), // unwanted "deeper" dependency
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  resolve: {
    extensions: ['', '.js', '.jsx', '.json'],
    alias: {
      config: path.join(__dirname, 'src', 'config', 'development')
    }
  },
  module: {
    loaders: [{
      test: /\.js$/,
      loaders: ['babel'],
      include: path.join(__dirname, 'src')
    },
    {
      test:   /\.css$/,
      loader: "style-loader!css-loader!postcss-loader"
    },
    {
      test:   /\.json$/,
      loader: "json-loader"
    }
  ]
  },
  postcss: function () {
    return [ autoprefixer ];
  }
};
