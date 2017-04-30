export const convertArrToGeojsonPoints = (dataArr, lngAccessor, latAccessor) => {
    let outFeatures = dataArr.map(d => {
        return {
            type: 'Feature',
            // properties: d,
            geometry: {"type":"Point","coordinates":[d[lngAccessor], d[latAccessor]]}
        }
    });

    return {
        "type":"FeatureCollection",
        "features":outFeatures
    }

};
