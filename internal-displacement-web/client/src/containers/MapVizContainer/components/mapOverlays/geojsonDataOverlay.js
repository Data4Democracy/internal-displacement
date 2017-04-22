import React, {Component} from 'react';
import 'babel-polyfill';
import DeckGL, {GeoJsonLayer} from 'deck.gl';
import * as d3 from 'd3';
import {convertArrToGeojsonPoints} from './../../../../utils/convertDataToGeojson';

export default class GeojsonCustomOverlay extends Component {

    static get defaultViewport() {
        return {
            latitude: 0,
            longitude: 0,
            zoom: 5,
            maxZoom: 16,
            pitch: 45,
            bearing: 0
        };
    }

    _initialize(gl) {
        gl.enable(gl.DEPTH_TEST);
        gl.depthFunc(gl.LEQUAL);
    }

    _getRadiusScale(maxRadius, maxDataValue) {
        return d3.scaleSqrt().domain([0, maxDataValue]).range([20, maxRadius])
    }

    render() {
        const {viewport, data, maxRadius, radiusAccessor} = this.props;

        if (!data) {
            return null;
        }

        console.log('rendering data')

        let maxRadiusData = d3.max(data,  d => d[radiusAccessor]);
        let radiusScale = this._getRadiusScale(maxRadius, 50);
        // let radiusScale = this._getRadiusScale(maxRadius, maxRadiusData);
        data.forEach(d => {
            d.radius = 50,//radiusScale(d.count);
            d.color =  [31, 186, 214, 255]
        });
        let geojsonMapData = convertArrToGeojsonPoints(data, 'long', 'lat');

        let testData = {
            "type": "FeatureCollection",
            "features": geojsonMapData.features.slice(0,5)
        };

        console.log('geojson', geojsonMapData, JSON.stringify(testData));

        const layer = new GeoJsonLayer({
            id: 'geojson',
            data: geojsonMapData,
            opacity: 0.8,
            visible: true,
            // stroked: false,
            filled: true,
            getRadius: d => d.properties.radius,
            getFillColor: d => [31, 186, 214, 100],
            // pickable: true,
            // onHover: () => {console.log('on hohver')}//this.props.onHover
        });

        return (
            <DeckGL {...viewport} layers={ [layer] } onWebGLInitialized={this._initialize} />
                );
    }
}