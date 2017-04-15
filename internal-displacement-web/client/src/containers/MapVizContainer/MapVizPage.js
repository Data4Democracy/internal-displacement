import React, {Component} from 'react';
import { dummyMapData, testDB} from './../../Api/api';
import './mapbox-gl.css'; //importing here since there are issues with webpack building mapbox-gl
import './mapVis.css';
import  {RenderMap } from './components/map';
import {loadIDData, updateMap} from './actions';
import reducer from './reducers/mapReducers'


class MapVizPage extends  Component {
    constructor(props) {
        super(props);
        this.state = {
            width: window.innerWidth,
            height: window.innerHeight,
        };
        window.addEventListener('resize', () => this.setState({width: window.innerWidth}));
    }

    componentWillMount() {
    // componentDidMount() {
    //     dummyMapData().then(data => {
    //         console.log(data);
    //         this.props.dispatch(loadIDData(data))
    //         this.setState({mapData: data})
    //     });
        // console.log(RenderMap)
    }

    render() {
        console.log(this.state.width);
        // return (<div>Map here</div>)
        return (RenderMap({width: this.state.width, height: this.state.height, latitude: 0, longitude: 0, zoom:0}))
    }

}

MapVizPage.propTypes = {

};
MapVizPage.defaultProps = {

};

export default MapVizPage