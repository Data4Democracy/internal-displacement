
import React, {Component} from 'react';
import {render} from 'react-dom';
import mapboxgl from 'mapbox-gl';
import * as d3 from 'd3';
import { MAPBOX_ACCESS_TOKEN } from './../../constants/mapConstants';

export const renderMap = (data, containerID = 'map', centerLat = 0, centerLng = 0, zoom=0, maxCount, minCount, maxRadius, minRadius) => {
    mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;
    let map = new mapboxgl.Map({
        container: containerID,
        style: 'mapbox://styles/mapbox/light-v9',
        center: [centerLng, centerLat],
        zoom: zoom
    });

    map.on('load', () => {
        map.addSource('idData', {
            'type': 'geojson',
            'data': data
        });

        map.addLayer({
            'id': 'idData-circles',
            'type': 'circle',
            'source': 'idData',
            'paint': {
                'circle-color': {
                    property: 'mag',
                    stops: [
                        [6, '#FCA107'],
                        [8, '#7F3121']
                    ]
                },
                'circle-opacity': 0.75,
                'circle-radius': {
                    property: 'radius',
                    "type": "exponential",
                    "stops": [
                        [{ "zoom": 0, "value": 1 }, 10],
                        [{ "zoom": 0, "value": 10 }, 50],
                        [{ "zoom": 0, "value": 100 }, 100],
                        [{ "zoom": 5, "value": 1 }, 20],
                        [{ "zoom": 5, "value": 10 }, 60],
                        [{ "zoom": 5, "value": 100 }, 110],
                        [{ "zoom": 10, "value": 1 }, 30],
                        [{ "zoom": 10, "value": 10 }, 70],
                        [{ "zoom": 10, "value": 100 }, 120],
                        [{ "zoom": 15, "value": 1 }, 40],
                        [{ "zoom": 15, "value": 10 }, 80],
                        [{ "zoom": 15, "value": 100 }, 130],
                        [{ "zoom": 20, "value": 1 }, 50],
                        [{ "zoom": 20, "value": 10 }, 90],
                        [{ "zoom": 20, "value": 100 }, 140]
                    ]
                }
            }
        });
    });
};
export const renderVisualizationOverlay = (data) => {
    //
    // const param = {
    //     props: this.props,
    //     state: this.state,
    // //     onWebGLInitialized: this._onWebGLInitialized,
    // //     effects: this._effects,
    // }

    if (data) {

    return (
        <div>

        </div>
    )
    } else {
        return( <div></div> )
    }
};
export const RenderMap = (props) => {
    console.log(props)

    if ( !props.mapData || props.mapData.length === 0) {
        return (

            <MapGL
                mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
                width={props.width}
                height={props.height}
                latitude={props.latitude}
                longitude={props.longitude}
                zoom={props.zoom}

                mapStyle='mapbox://styles/mapbox/light-v9'

            >
                <div>Map rendering</div>
            </MapGL>
        );
    }

    return (

        <MapGL
            mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
            width={props.width}
            height={props.height}
            latitude={props.latitude}
            longitude={props.longitude}
            zoom={props.zoom}

            mapStyle='mapbox://styles/mapbox/light-v9'

        >
            {renderVisualizationOverlay(props)}
        </MapGL>
        // <MapGL
        //     mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
        //     width={props.width}
        //     height={props.height}
        //     mapStyle='mapbox://styles/mapbox/dark-v9'
        //     perspectiveEnabled
        //     //{ ...props.mapViewState }
        //     // onChangeViewport={ props.handleViewportChanged }
        //onChangeViewport={viewport => {
    // const {latitude, longitude, zoom} = viewport;
    // Optionally call `setState` and use the state to update the map.
// }}
        // >
        //     {/*{isActiveOverlay && this._renderVisualizationOverlay()}*/}
        // </MapGL>
    );
    // return (<div>Maop here!!!</div>)
};


// export default RenderMap