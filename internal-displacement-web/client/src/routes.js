import React from 'react';
import {Route, IndexRoute }from 'react-router';
import App from './containers/app';
import HomePage from './components/HomePage';
import MapVizPage from './containers/MapVizContainer/MapVizPage';

export default (
	<Route path='/' component={App}>
		<IndexRoute component={HomePage}/>
		<Route path='/mapViz' component={MapVizPage}/>
	</Route>
)