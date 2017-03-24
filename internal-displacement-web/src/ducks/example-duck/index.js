import { createAction, createReducer } from 'redux-act'

export const createSpaceRequest = createAction('space/create/request')

export const createSpace = (space) => {
  return dispatch => {
    dispatch(createSpaceRequest(space))

    return axios.post(`${GENISYS_FACTORY_SERVICE_URL}/v1/spaces`, space, getRequestAuthHeader())
      .then(({ data }) => dispatch(createSpaceSuccess(data)))
      .catch(error => dispatch(createSpaceFailure(error)))
  }
}

const initialState = {
  busy: false,
  error: null,
}

export default createReducer({
  [createSpaceRequest]: (state) => ({
    ...state,
    busy: true,
    error: null,
  }),
}, initialState )
