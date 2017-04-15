// import { put, call } from 'redux-saga/effects';
// import { dummyMapData } from './../../../Api/api';
//
// export function* mapDataSaga({ payload }) {
//     try {
//         const mapData = yield call(dummyMapData, payload);
//         yield [
//             put({ type: 'LOAD_ID_DATA_SUCCESS', mapData })
//         ];
//     } catch (error) {
//         yield put({ type: 'LOAD_MAPDATA_ERROR', error });
//     }
// }