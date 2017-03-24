import React from 'react'
import { storiesOf, action } from '@kadira/storybook'

import InternalDisplacement from '../src'

storiesOf('InternalDisplacement', module)
  .addWithInfo('Basic', 'added Description', () => (
    <InternalDisplacement />
  ), { inline: true })
  .add('Basic', () => (
    <InternalDisplacement />
  ))
