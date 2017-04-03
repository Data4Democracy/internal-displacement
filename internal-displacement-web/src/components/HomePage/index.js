import React from 'react';
import { Link } from 'react-router';

const HomePage = () => (
	<div className="jumbotron center">
		<h1 className="lead">Internal Displacement </h1>
		<div>
			<Link to="mapviz">
				<button className="btn btn-lg btn-primary"> Map</button>
			</Link>
			<Link to="article-submission">
				<button className="btn btn-lg btn-primary">Submit a link</button>
			</Link>
			<Link to="analyses">
				<button className="btn btn-lg btn-primary"> Analytics</button>
			</Link>
		</div>
	</div>
);

export default HomePage;