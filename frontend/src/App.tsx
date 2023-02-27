import MapChart from './MapChart';
import { ThemeProvider } from './ThemeProvider';
import { useState, useEffect } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css'

export interface CountryStats {
  name: string;
  population: number;
  capital: string;
  gini_index: number;
}

export default function App() {
  const [tooltipContent, setTooltipContent] = useState('test');
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [countryStats, setCountryStats] =
    useState<CountryStats>({ name: '', population: 0, capital: '', gini_index: 0 });

  function onMouseUpdate(e: MouseEvent) {
    setTooltipPosition({ x: e.pageX, y: e.pageY });
  }

  useEffect(() => {
    document.addEventListener('mousemove', onMouseUpdate, false);
    document.addEventListener('mouseenter', onMouseUpdate, false);
    return () => {
      document.removeEventListener('mousemove', onMouseUpdate);
      document.removeEventListener('mouseenter', onMouseUpdate);
    };
  }, []);

  return (
    <ThemeProvider>
      <MapChart
        setTooltipContent={setTooltipContent}
        setTooltipPosition={setTooltipPosition}
        setCountryStats={setCountryStats}
      />
      <Tooltip id="map-tooltip" position={tooltipPosition}>
        {countryStats.name}
        <ul>
          <li>population: {countryStats.population}</li>
          <li>capital: {countryStats.capital}</li>
          <li>gini index: {countryStats.gini_index}</li>
        </ul>
      </Tooltip>
    </ThemeProvider>
  );
}
