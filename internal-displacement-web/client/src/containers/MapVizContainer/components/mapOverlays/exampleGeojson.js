import React, {Component} from 'react';

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
            latitude: 49.254,
            longitude: -123.13,
            zoom: 11,
            maxZoom: 16,
            pitch: 0,
            bearing: 0
        };
    }

    _initialize(gl) {
        gl.enable(gl.DEPTH_TEST);
        gl.depthFunc(gl.LEQUAL);
    }

    render() {
        const {viewport, data, colorScale} = this.props;

        if (!data) {
            return null;
        }

        const layer = new GeoJsonLayer({
            id: 'geojson',
            data,
            opacity: 0.8,
            stroked: false,
            filled: true,
            extruded: true,
            wireframe: true,
            fp64: true,
            //getElevation: f => Math.sqrt(f.properties.valuePerSqm) * 10,
            // getFillColor: f => colorScale(f.properties.growth),
            // getLineColor: f => [255, 255, 255],
            getRadius: d => 2050,
            getFillColor: d => [31, 186, 214, 100],
            lightSettings: LIGHT_SETTINGS,
            pickable: Boolean(this.props.onHover),
            onHover: this.props.onHover
        });

        return (
            <DeckGL {...viewport} layers={ [layer] } onWebGLInitialized={this._initialize} />
        );
    }
}