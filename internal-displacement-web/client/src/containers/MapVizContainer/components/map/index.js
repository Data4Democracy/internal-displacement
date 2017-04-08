
import React from 'react';
import MapGL from 'react-map-gl';
// import MapboxGLMap from 'react-map-gl';
import { MAPBOX_ACCESS_TOKEN } from './../../constants/mapConstants';

const RenderMap = (props) => {
    return (
        <MapGL
            mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
            width={props.width}
            height={props.height}
            mapStyle='mapbox://styles/mapbox/dark-v9'
            perspectiveEnabled
            //{ ...props.mapViewState }
            // onChangeViewport={ props.handleViewportChanged }
        >
            {/*{isActiveOverlay && this._renderVisualizationOverlay()}*/}
        </MapGL>
    );
};

export default RenderMap