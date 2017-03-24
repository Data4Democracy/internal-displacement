import React from 'react'
import { Route, IndexRoute } from 'react-router'
import App from '../containers/app'
import Home from '../containers/home'
import NotFound from '../components/NotFound'

export default (
  <Route>
    <Route path="/" component={App}>
      <IndexRoute component={Home} />
    </Route>
    <Route path="*" status={404} component={NotFound} />
  </Route>
)
