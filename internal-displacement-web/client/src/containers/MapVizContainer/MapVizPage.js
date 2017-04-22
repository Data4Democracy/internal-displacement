import React, {Component} from 'react';
import {render} from 'react-dom';

import { dummyMapData, testDB} from './../../Api/api';
import './mapbox-gl.css'; //importing here since there are issues with webpack building mapbox-gl
import './mapVis.css';

import mapboxgl from 'mapbox-gl';

import  {RenderMap } from './components/map';
import {loadIDData, updateMap} from './actions';
import {createStore} from 'react-redux';

import "babel-polyfill";
import MapGL from 'react-map-gl';


import { MAPBOX_ACCESS_TOKEN } from './constants/mapConstants';
import GeojsonCustomOverlay from './components/mapOverlays/geojsonDataOverlay';

class MapVizPage extends  Component {
    constructor(props) {
        super(props);
        this.state = {

            data: null,
            // mapData: [],
            viewport: {
                ...GeojsonCustomOverlay.defaultViewport,
                startDragLngLat: null,
                isDragging: false,
                width: window.innerWidth,
                height: window.innerHeight,
            },
            maxRadius: 20,
            radiusAccessor: 'count'
        };
        window.addEventListener('resize', () => this.setState({width: window.innerWidth}));
    }

    componentDidMount() {
        window.addEventListener('resize', this._resize.bind(this));
        console.log(mapboxgl, 'mapbox exists?', window)
        this._resize();
        let self = this;
    // componentDidMount() {
        dummyMapData().then(data => {
            console.log('data', self.state, self.setState);
            let parsed = JSON.parse(data).rows;
            // this.props.dispatch(loadIDData(data))
            self.setState({data: parsed})
        });

    }

    _resize() {
        this._onChangeViewport({
            width: window.innerWidth,
            height: window.innerHeight
        });
    }

    render() {
        const {viewport, data, maxRadius, radiusAccessor} = this.state;

        return (
            <MapGL
                {...viewport}
                perspectiveEnabled={true}
                onChangeViewport={this._onChangeViewport.bind(this)}
                mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}>

                <GeojsonCustomOverlay
                    viewport={viewport}
                    data={data}
                    radiusAccessor={radiusAccessor}
                    maxRadius={200}
                />
                <div>Geojson Custom overlay</div>
            </MapGL>
        )


    }

    _onChangeViewport(viewport) {
        this.setState({
            viewport: {...this.state.viewport, ...viewport}
        });
    }

}

MapVizPage.propTypes = {

};
MapVizPage.defaultProps = {

};

export default MapVizPage