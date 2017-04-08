import React, {Component} from 'react';
import { dummyMapData, testDB} from './../../Api/api';
import MapboxGLMap from 'react-map-gl';
import { MAPBOX_ACCESS_TOKEN } from './constants/mapConstants';
import { RenderMap } from './components/map';


class MapVizPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
			width: window.innerWidth,
			height: window.innerHeight
        };
        window.addEventListener('resize', () => this.setState({width: window.innerWidth}));
    }

	componentDidMount() {
		dummyMapData().then(data => {
			console.log(data);
		});
	}

	render() {
		return (<div>{RenderMap({width:800, height:400})}</div>)
	}

    renderTEst() {

        return (
			<div>
                { this._renderMap() }
				<div className='overlay-contol-container'>
					{/*<MapSelection {...mapSelectionProps}/>*/}
					{/*<LayerInfo {...layerInfoProps}/>*/}
				</div>
			</div>
        )
    }

    _renderMap() {
        const { mapViewState } = this.props;
        const { width, height } = this.state;
        return (
			<MapboxGLMap
				mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
				width={width}
				height={height}
				mapStyle='mapbox://styles/mapbox/dark-v9'
				perspectiveEnabled
                { ...mapViewState }
                onChangeViewport={this._handleViewportChanged}
			>
                {/*{isActiveOverlay && this._renderVisualizationOverlay()}*/}
			</MapboxGLMap>
        );
    }

}

MapVizPage.propTypes = {

};
MapVizPage.defaultProps = {

};

export default MapVizPage