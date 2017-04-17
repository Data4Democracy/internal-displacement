
import React from 'react';
import MapGL from 'react-map-gl';
// import MapboxGLMap from 'react-map-gl';
import { MAPBOX_ACCESS_TOKEN } from './../../constants/mapConstants';
import HeatMapOverlayRender from './../mapOverlays/displacementHeatmapOverlay';

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

            {HeatMapOverlayRender(data) }
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