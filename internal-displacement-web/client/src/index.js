import React from 'react';
import ReactDOM from 'react-dom';
import { Router, browserHistory } from 'react-router';
import routes from './routes';
import Bootstrap from 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import { Provider } from 'react-redux';
import {createStore} from 'redux';
import mapReducer from './containers/MapVizContainer/reducers/mapReducers';

const store = createStore(mapReducer);

// We require the routes and render to the DOM using ReactDOM API
ReactDOM.render(
	<Provider store={store}>
	<Router history={browserHistory} routes={routes} /></Provider>,
	document.getElementById('root')
);
