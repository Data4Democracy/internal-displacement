/* global window,document */
import React, {Component} from 'react';
import {render} from 'react-dom';
import MapGL from 'react-map-gl';
import DeckGLOverlay from './components/mapOverlays/exampleGeojson.js';
import { MAPBOX_ACCESS_TOKEN } from './constants/mapConstants';
import customData from './vancouver-blocks.json';

import { dummyMapData} from './../../Api/api';
import {convertArrToGeojsonPoints} from './../../utils/convertDataToGeojson';

// Set your mapbox token here
const MAPBOX_TOKEN = MAPBOX_ACCESS_TOKEN; // eslint-disable-line

const colorScale = r => [r * 255, 140, 200 * (1 - r)];

class MapVizPageTest extends Component {

    constructor(props) {
        super(props);
        this.state = {
            viewport: {
                ...DeckGLOverlay.defaultViewport,
                width: 500,
                height: 500
            },
            data: null
        };


        // requestJson('./vancouver-blocks.json', (error, response) => {
        //     if (!error) {
        //         this.setState({data: response});
        //     }
        // });
    }

    componentDidMount() {
        window.addEventListener('resize', this._resize.bind(this));
        this._resize();
        let self=this;
        if (customData) {
            console.log(customData)
            let plotData = {
                "type": "FeatureCollection",
                "features": []
            };
            plotData.features = customData.features.map(d => {
                return {"type":"Feature","geometry":{"type":"Point","coordinates": d.geometry.coordinates[0][0]}}
            });

            dummyMapData().then(data => {
                console.log('data');
                let parsed = JSON.parse(data).rows;
                let parsedGeojson = convertArrToGeojsonPoints(parsed, 'long', 'lat')
                // this.props.dispatch(loadIDData(data))
                self.setState({data: parsedGeojson})
            });
            this.setState({data: plotData});
        }
    }

    _resize() {
        this._onChangeViewport({
            width: window.innerWidth,
            height: window.innerHeight
        });
    }

    _onChangeViewport(viewport) {
        this.setState({
            viewport: {...this.state.viewport, ...viewport}
        });
    }

    render() {
        const {viewport, data} = this.state;

        return (
            <MapGL
                {...viewport}
                perspectiveEnabled={true}
                onChangeViewport={this._onChangeViewport.bind(this)}
                mapboxApiAccessToken={MAPBOX_TOKEN}>
                <DeckGLOverlay viewport={viewport}
                               data={data}
                               colorScale={colorScale} />
            </MapGL>
        );
    }
}

export default MapVizPageTest
