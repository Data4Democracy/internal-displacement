import React, {Component} from 'react';
import { dummyMapData, reportLocationData} from '../Api/api';

class MapVizPage extends Component {
	componentDidMount() {
		dummyMapData().then(data => {
			console.log(data);
		});
        reportLocationData().then(data => {
        	console.log('report llocation data', data);
		})
	}

	render() {
		return (<div>Map here</div>)
	}
}

export default MapVizPage