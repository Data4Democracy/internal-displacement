import React, {Component} from 'react';
import 'babel-polyfill';
import DeckGL, {GeoJsonLayer} from 'deck.gl';

const LIGHT_SETTINGS = {
    lightsPosition: [-125, 50.5, 5000, -122.8, 48.5, 8000],
    ambientRatio: 0.2,
    diffuseRatio: 0.5,
    specularRatio: 0.3,
    lightsStrength: [1.0, 0.0, 2.0, 0.0],
    numberOfLights: 2
};

export default class DeckGLOverlay extends Component {

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

    render() {
        const {viewport, mapData, radiusScale} = this.props;

        if (!mapData) {
            return null;
        }

        const layer = new GeoJsonLayer({
            id: 'geojson',
            data: mapData,
            opacity: 0.5,
            radiusScale: 4,
            radiusMinPixels: 0.25,
            getPosition: d => [d[0], d[1], 0],
            getRadius: d => 5,
            getColor: d => "#1FBAD6",
            // stroked: false,
            // filled: true,
            // extruded: true,
            // wireframe: true,
            // fp64: true,
            // getElevation: f => Math.sqrt(f.properties.valuePerSqm) * 10,
            // getFillColor: f => colorScale(f.properties.growth),
            // getLineColor: f => [255, 255, 255],
            lightSettings: LIGHT_SETTINGS,
            pickable: Boolean(this.props.onHover),
            onHover: this.props.onHover
        });

        return (
            <DeckGL {...viewport} layers={ [layer] } onWebGLInitialized={this._initialize} />
        );
    }
}