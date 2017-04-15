import React, {Component} from 'react';
import { dummyMapData, testDB} from './../../Api/api';
import './mapbox-gl.css'; //importing here since there are issues with webpack building mapbox-gl
import './mapVis.css';
import  {RenderMap } from './components/map';
import {loadIDData, updateMap} from './actions';
import {createStore} from 'react-redux';

// const store = createStore(mapReducer);

class MapVizPage extends  Component {
    constructor(props) {
        super(props);
        this.state = {
            width: window.innerWidth,
            height: window.innerHeight,
            mapData: []
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
            self.setState({mapData: parsed})
            self.state.mapData = data
        });

        // console.log(RenderMap)
    }

    render() {
        console.log(this.state);
        // return (<div>Map here</div>)
        return (

            RenderMap({
                width: this.state.width,
                height: this.state.height,
                latitude: 0, longitude: 0,
                zoom:0,
                mapData: this.state.mapData})
        )
    }

}

MapVizPage.propTypes = {

};
MapVizPage.defaultProps = {

};

export default MapVizPage