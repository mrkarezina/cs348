import { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import 'semantic-ui-css/semantic.min.css';
import { Container, Dropdown, Table } from 'semantic-ui-react';
import { CountryStats, fetchCountryInfo } from './apiCalls';
import MapChart from './MapChart';
import { ThemeProvider } from './ThemeProvider';
import { countryOptions } from './Countries';

export default function App() {
  const [tooltipStats, setTooltipStats] = useState<CountryStats | null>(null);
  const [countryStats, setCountryStats] = useState<CountryStats | null>(null);

  return <>
    <ThemeProvider>
      <MapChart
        setTooltipStats={setTooltipStats}
        setCountryStats={setCountryStats}
        countryStats={countryStats}
      />
      <Tooltip id='map-tooltip' float offset={20}>
        {tooltipStats !== null && <>
          {tooltipStats.name}
          <ul>
            <li>population: {tooltipStats.population}</li>
            <li>capital: {tooltipStats.capital}</li>
            <li>gini index: {tooltipStats.giniIndex}</li>
          </ul>
        </>
        }
      </Tooltip>
    </ThemeProvider>
    <Container>
      <Dropdown
        placeholder='Search country'
        fluid
        search
        selection
        onChange={async (event, data) => {
          const country_stats = await fetchCountryInfo({ code: data.value?.toString() || '' });
          setCountryStats(country_stats);
        }}
        text={countryStats?.name}
        options={countryOptions}
      />
      {countryStats && <Table celled>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell>Stat</Table.HeaderCell>
            <Table.HeaderCell>Value</Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>
          <Table.Row>
            <Table.Cell>Name</Table.Cell>
            <Table.Cell>{countryStats?.name}</Table.Cell>
          </Table.Row>
          <Table.Row>
            <Table.Cell>Population</Table.Cell>
            <Table.Cell>{countryStats?.population}</Table.Cell>
          </Table.Row>
          <Table.Row>
            <Table.Cell>Capital City</Table.Cell>
            <Table.Cell>{countryStats?.capital}</Table.Cell>
          </Table.Row>
          <Table.Row>
            <Table.Cell>Gini Index</Table.Cell>
            <Table.Cell>{countryStats?.giniIndex}</Table.Cell>
          </Table.Row>
        </Table.Body>
      </Table>
      }
    </Container>
  </>;
}
