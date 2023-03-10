import { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import 'semantic-ui-css/semantic.min.css';
import { Container, Dropdown } from 'semantic-ui-react';
import { CountryStats, fetchCountryInfo } from './apiCalls';
import MapChart from './MapChart';
import { ThemeProvider } from './ThemeProvider';
import { countryOptions } from './Countries';

export default function App() {
  const [tooltipStats, setTooltipStats] = useState<CountryStats | null>(null);
  const [countryStats, setCountryStats] = useState<CountryStats | null>(null);

  return <>
    <ThemeProvider>
      <Container style={{ margin: 18, width: 400 }}>
        <Dropdown
            placeholder='Search country'
            fluid
            search
            selection
            onChange={async (event, data) => {
              const country_stats = await fetchCountryInfo({ code: data.value?.toString().toUpperCase() || '' });
              setCountryStats(country_stats);
            }}
            text={countryStats?.name}
            options={countryOptions}
        />
      </Container>
      <Container style={{ width: 2000, height: 900 }}>
        <MapChart
          setTooltipStats={setTooltipStats}
          setCountryStats={setCountryStats}
          countryStats={countryStats}
        />
      </Container>
      <Tooltip id='map-tooltip' float offset={20}>
        {tooltipStats?.name &&
          <>
            <h3>{tooltipStats.name}</h3>
            {tooltipStats.population && <div>{`Population: ${tooltipStats.population}`}</div>}
            {tooltipStats.area && <div>{`Area: ${tooltipStats.area}`}</div>}
            {tooltipStats.giniIndex && <div>{`Gini Index: ${tooltipStats.giniIndex}`}</div>}
            {tooltipStats.gdp && <div>{`GDP: ${tooltipStats.gdp}`}</div>}
            {tooltipStats.education_epd && <div>{`Education Expenditure: ${tooltipStats.education_epd}`}</div>}
            {tooltipStats.unemployment_rate && <div>{`Unemployment Rate: ${tooltipStats.unemployment_rate}`}</div>}
          </>
        }
      </Tooltip>
    </ThemeProvider>
  </>;
}
