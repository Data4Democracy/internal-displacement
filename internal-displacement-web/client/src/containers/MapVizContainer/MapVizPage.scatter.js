import React, {Component} from 'react';
import { dummyMapData, testDB} from './../../Api/api';
import './mapbox-gl.css'; //importing here since there are issues with webpack building mapbox-gl
import './mapVis.css';
import  {RenderMap } from './components/map';
import {loadIDData, updateMap} from './actions';
import {createStore} from 'react-redux';
import "babel-polyfill";
import MapGL, {autobind} from 'react-map-gl';

import DeckGL, {LineLayer} from 'deck.gl';
// const store = createStore(mapReducer);
// import MapboxGLMap from 'react-map-gl';
import { MAPBOX_ACCESS_TOKEN } from './constants/mapConstants';
import HeatMapOverlayRender from './components/mapOverlays/displacementHeatmapOverlay';
import {DeckGLOverlay} from './components/mapOverlays/geojsonDataOverlay';
import ScatterLayer from './components/mapOverlays/scatterplotOverlay';
class MapVizPageScatter extends  Component {
    constructor(props) {
        super(props);
        this.state = {

            data: null,
            // mapData: [],
            viewport: {
                latitude: 0,
                longitude: 0,
                zoom: 0,
                startDragLngLat: null,
                isDragging: false,
                width: window.innerWidth,
                height: window.innerHeight,
            }
        };
        window.addEventListener('resize', () => this.setState({width: window.innerWidth}));
    }

    componentDidMount() {
        let self = this;
    // componentDidMount() {
        dummyMapData().then(data => {
            console.log('data', self.state, self.setState);
            let parsed = JSON.parse(data).rows;
            // this.props.dispatch(loadIDData(data))
            self.setState({data: parsed.map(d => {
                return {
                   position: [d.long, d.lat],
                    radius: d.count
                }})})
            // self.setState({data: parsed})
        });

        // console.log(RenderMap)
    }

    _resize() {
        this._onChangeViewport({
            width: window.innerWidth,
            height: window.innerHeight
        });
    }

    render() {
        let mapProps = {
            ...this.state.viewport,
            // ...this.state.mapData
        };
        const {viewport, data} = this.state;

        // return (
        //     <MapGL
        //         {...viewport}
        //         perspectiveEnabled={true}
        //         onChangeViewport={this._onChangeViewport.bind(this)}
        //         mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}>
        //         <DeckGLOverlay viewport={viewport}
        //                        data={data}
        //                        radius={30}
        //         />
        //     </MapGL>
        // );

        return (
            <MapGL
                {...viewport}
                perspectiveEnabled={true}
                onChangeViewport={this._onChangeViewport.bind(this)}
                mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}>
                <ScatterLayer viewport={viewport}
                               data={data}
                               radius={30}
                />
            </MapGL>
        )

        if ( !this.state.mapData || this.state.mapData.length === 0) {
            return (

                <MapGL
                    mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
                    {...mapProps}
                    perspectiveEnabled={true}
                    onChangeViewport={this._onChangeViewport.bind(this)}

                    mapStyle='mapbox://styles/mapbox/light-v9'

                >
                    <div>Map rendering</div>
                </MapGL>
            );
        }

        return (

            <MapGL
                mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN}
                {...mapProps}
                mapStyle='mapbox://styles/mapbox/light-v9'
            >

                    {HeatMapOverlayRender({...this.state.viewport, mapData: this.state.mapData}) }

            </MapGL>
        );
    }

    _onChangeViewport(viewport) {
        this.setState({
            viewport: {...this.state.viewport, ...viewport}
        });
    }

}



export default MapVizPageScatter