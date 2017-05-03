
// actions for map
export const updateMap = (mapViewState)  => {
    return {type: 'UPDATE_MAP', mapViewState};
};

export const loadIDData = (data) => {
    return {type: 'LOAD_ID_DATA_SUCCESS', data};
};



