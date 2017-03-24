import { routerReducer } from 'react-router-redux'
import { applyMiddleware, combineReducers, createStore } from 'redux'
import createLogger from 'redux-logger'
import thunk from 'redux-thunk'

import exampleDuck from '../ducks/example-duck'

const reducers = combineReducers({
  routing: routerReducer,
  exampleDuck: exampleDuck,
})

const logger = createLogger()
const createStoreWithMiddleware = applyMiddleware(thunk, logger)
const store   = createStore(reducers, createStoreWithMiddleware)

export default store
