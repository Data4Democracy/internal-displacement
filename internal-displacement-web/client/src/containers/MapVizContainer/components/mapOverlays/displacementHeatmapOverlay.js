import React, { Component } from 'react';
import Immutable from 'immutable';
// import DeckGL from 'deck.gl';
// import HeatmapOverlay from 'react-map-gl-heatmap-overlay';
import {ScatterplotOverlay} from 'react-map-gl';



const HeatMapOverlayRender = (param) => {
    console.log('heatmapoverlay render', param.mapData.map(d => [d.long, d.lat]))
    const idData = Immutable.fromJS(param.mapData);
    // const idData = Immutable.fromJS(param.mapData.map(d => [d.long, d.lat]));
    const width = param.width;
    const height = param.height;
    const zoom = param.zoom || 0;
    // const { width, height,  mapViewState  } = param;
    return (
    //     <HeatmapOverlay
    //         locations={idData}
    //         {...mapViewState}
    //         width={width}
    //         height={height}
    //         lngLatAccessor={(data) => [data.long, data.lat]}
    //     />
        <ScatterplotOverlay
            latitude={0}
            longitude={0}
            width={width}
            height={height}
            zoom={zoom}
            isDragging={true}
            locations={idData}
            dotRadius={4}
            globalOpacity={1}
            compositeOperation="screen"
            dotFill="#1FBAD6"
            renderWhileDragging={true}
            lngLatAccessor={(data) => [data.get('long'), data.get('lat')]}
        />
    )


};

export default HeatMapOverlayRender;