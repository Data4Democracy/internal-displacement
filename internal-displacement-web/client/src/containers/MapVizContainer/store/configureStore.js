// import { createStore, applyMiddleware } from 'redux';
// import createSagaMiddleware from 'redux-saga';
// import reducer from './../reducers/mapReducers';
// import rootSaga from './../sagas'; // TODO: Next step
//
// //  Returns the store instance
// // It can  also take initialState argument when provided
// const configureStore = () => {
//     const sagaMiddleware = createSagaMiddleware();
//     return {
//         ...createStore(reducer,
//             applyMiddleware(sagaMiddleware)),
//         runSaga: sagaMiddleware.run(rootSaga)
//     };
// };
//
// export default configureStore;