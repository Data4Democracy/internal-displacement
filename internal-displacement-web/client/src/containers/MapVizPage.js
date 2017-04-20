import React, {Component} from 'react';
import { dummyMapData} from '../Api/api';

class MapVizPage extends Component {
	componentDidMount() {
		dummyMapData().then(data => {
			console.log(data);
		});
	}

	render() {
		return (<div>Map here</div>)
	}
}

export default MapVizPage