import initialState from './initialState';

export default function (state = initialState, action) {
    switch (action.type) {
        case 'UPDATE_MAP':
            return {...state, mapViewState: action.mapViewState};
        case 'LOAD_ID_DATA_SUCCESS':
            return { ...state, displacementData: action.displacementData };
        default:
            return state;
    }
}