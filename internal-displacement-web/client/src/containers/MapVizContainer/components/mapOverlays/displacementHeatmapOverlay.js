import React, { Component } from 'react';
// import DeckGL from 'deck.gl';
// import HeatmapOverlay from 'react-map-gl-heatmap-overlay';
import {ScatterPlotOverlay} from 'react-map-gl';



const HeatMapOverlayRender = (param) => {
    console.log('heatmapoverlay render', param)
    const { idData} = param.mapData;
    const { width, height,  mapViewState  } = param.state;
    return (
    //     <HeatmapOverlay
    //         locations={idData}
    //         {...mapViewState}
    //         width={width}
    //         height={height}
    //         lngLatAccessor={(data) => [data.long, data.lat]}
    //     />
        <ScatterPlotOverlay
            {...mapViewState}
            locations={idData}
            dotRadius={4}
            globalOpacity={1}
            compositeOperation="screen"
            dotFill="#1FBAD6"
            renderWhileDragging={true}
            lngLatAccessor={(data) => [data.long, data.lat]}
        />
    )


};

export default HeatMapOverlayRender;