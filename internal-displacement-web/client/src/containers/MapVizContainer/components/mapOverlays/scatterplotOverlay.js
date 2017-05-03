import React, {Component} from 'react';
import DeckGL, {ScatterplotLayer} from 'deck.gl';

export default class ScatterLayer extends Component {

    static get defaultViewport() {
        return {
            longitude: -74,
            latitude: 40.7,
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
        console.log('rendering', DeckGL)
        const {viewport,  data, radius} = this.props;

        if (!data) {
            return null;
        }

        console.log('layer', data)
        const layer = new ScatterplotLayer({
            id: 'scatter-plot',
            data,
            pickable: true,
            //radiusScale: radius,
            radiusMinPixels: 2,
            radiusMaxPixels: 280,
            // radiusMinPixels
            getPosition: d => d.position,
            getRadius: d => d.radius,
            getColor: d => [0,0,0,100]
        });

        return (
            <DeckGL {...viewport} layers={ [layer] } onWebGLInitialized={this._initialize} />
        );
    }
}