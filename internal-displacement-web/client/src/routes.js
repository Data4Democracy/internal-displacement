import React from 'react';
import {Route, IndexRoute }from 'react-router';
import App from './containers/app';
import HomePage from './components/HomePage';
import MapVizPage from './containers/MapVizContainer/MapVizPage';
import MapVizPageTest from './containers/MapVizContainer/MapVizExample';
import MapVizPageScatter from './containers/MapVizContainer/MapVizPage.scatter';

let routes = (
	<Route path='/' component={App}>
		<IndexRoute component={HomePage}/>
		<Route path='/mapViz' component={MapVizPage}/>
		<Route path='/mapVizTest' component={MapVizPageTest}/>
		<Route path='/mapVizScatter' component={MapVizPageScatter}/>
	</Route>
);


export default (
	<Route path='/' component={App}>
		<IndexRoute component={HomePage}/>
		<Route path='/mapViz' component={MapVizPage}/>
		<Route path='/mapVizTest' component={MapVizPageTest}/>
		<Route path='/mapVizScatter' component={MapVizPageScatter}/>
	</Route>
)