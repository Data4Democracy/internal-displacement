import React from 'react';
import ReactDOM from 'react-dom';
import { Router, browserHistory } from 'react-router';
import routes from './routes';
import Bootstrap from 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

// We require the routes and render to the DOM using ReactDOM API
ReactDOM.render(
	<Router history={browserHistory} routes={routes} />,
	document.getElementById('root')
);
