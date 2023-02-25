import MapChart from './MapChart';
import { ThemeProvider } from './ThemeProvider';
import { Welcome } from './Welcome/Welcome';
import React, { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css'

export default function App() {
  const [content, setContent] = useState('test');
  return (
    <ThemeProvider>
      <MapChart setTooltipContent={setContent} />
      <Tooltip id='map-tooltip'>{content}</Tooltip>
    </ThemeProvider>
  );
}
