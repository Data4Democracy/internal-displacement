import React, { Component } from 'react';
import DeckGL from 'deck.gl';
import HeatmapOverlay from 'react-map-gl-heatmap-overlay';

const HeatMapOverlay = (props) => {
    const { idData} = props.idData;
    const { width, height,  mapViewState  } = props.state;
    return (
        <HeatmapOverlay
            locations={idData}
            {...mapViewState}
            width={width}
            height={height}
            lngLatAccessor={(data) => [data.long, data.lat]}
        />
    )
};

export default HeatmapOverlay;