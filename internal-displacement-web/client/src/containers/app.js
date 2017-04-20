import React, { Component, PropTypes } from 'react';
import Header from '../common/Header';
const propTypes = {
  children: PropTypes.element.isRequired,
};

export default class App extends React.Component {
  render() {
    return (
      <div className="container-fluid text-center">
        <Header />
        {this.props.children}
      </div>
    )
  }
}

App.propTypes = propTypes;
