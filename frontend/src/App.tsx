import { ActionIcon, Avatar, Button, Container, Divider, Drawer, Flex, Group, Modal, Radio, Select, Slider, Space, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import 'semantic-ui-css/semantic.min.css';
import { Dropdown } from 'semantic-ui-react';
import { CountryStats, fetchCountryInfo, getCountryRankings, getLeaderboard } from './apiCalls';
import { countryOptions } from './Countries';
import Game from './Game';
import Leaderboard from './Leaderboard';
import Login from './Login';
import MapChart from './MapChart';
import SignUp from './SignUp';
import { ThemeProvider } from './ThemeProvider';
import UserProfile from './UserProfile';
import { useCookie } from './utils';

const stats = [
  {value: 'area', label: 'Area'},
  {value: 'education_expenditure', label: 'Education expenditure'},
  {value: 'gini_index', label: 'Gini index'},
  {value: 'population', label: 'Population'},
  {value: 'real_gdp', label: 'GDP'},
  {value: 'unemployment_rate', label: 'Unemployment rate'},
]

const regions = [
  {value: '1', label: 'South America'},
  {value: '2', label: 'East and Southeast Asia'},
  {value: '3', label: 'Middle East'},
  {value: '4', label: 'Central America and the Caribbean'},
  {value: '5', label: 'Antarctica'},
  {value: '6', label: 'Central Asia'},
  {value: '7', label: 'Africa'},
  {value: '8', label: 'Australia and Oceania'},
  {value: '9', label: 'North America'},
  {value: '10', label: 'South Asia'},
  {value: '11', label: 'Europe'},
]

export default function App() {
  const [tooltipStats, setTooltipStats] = useState<CountryStats | null>(null);
  const [countryStats, setCountryStats] = useState<CountryStats | null>(null);
  const [rankingStat, setRankingStat] = useState<string | null>(null);
  const [rankingBatchNum, setRankingBatchNum] = useState<number | null>(null);
  const [rankingOrder, setRankingOrder] = useState<string | null>(null);
  const [rankingRegion, setRankingRegion] = useState<string | null>(null);

  const [username, setUsername] = useCookie('username', null);

  const [opened, { open, close }] = useDisclosure(false);
  const [drawerTitle, setDrawerTitle] = useState<string | null>(null);
  const [leftDrawerTitle, setLeftDrawerTitle] = useState<string | null>(null);


  return <>
    <ThemeProvider>
      {/* top bar */}
      <Flex justify={'flex-end'} style={{ marginTop: 8 }}>
          <Flex justify='space-around'>
            <Space w='sm' />
            <Button onClick={() => { getLeaderboard().then(info => setLeftDrawerTitle('Leaderboard')) }}>Leaderboard</Button>
            <Space w='sm' />
            <Button onClick={() => { setLeftDrawerTitle('Country Rankings') }}>Country</Button>
            <Space w='sm' />
            { username && <Button onClick={() => { setDrawerTitle('Game') }}>Start Game</Button> }
          </Flex>
          <Drawer title={leftDrawerTitle} position='left' opened={!!leftDrawerTitle} onClose={() => setLeftDrawerTitle(null)} >
            {leftDrawerTitle == 'Leaderboard' && <Leaderboard />}
            {leftDrawerTitle == 'Country Rankings' && <>
              <Flex direction={'column'} style={{ margin: 6 }}>
                <Select
                  label="Select stat name to rank the countries by"
                  onChange={setRankingStat}
                  defaultValue={"area"}
                  data={stats}
                  searchable
                />
                <Divider my="sm"/>
                <Space h='lg' />
                <Select
                  label="Select region"
                  data={regions}
                  onChange={setRankingRegion}
                  clearable
                  searchable
                />
                <Divider my="sm"/>
                <Space h='lg' />
                <Radio.Group
                  name="order"
                  label="Select Order"
                  description="Select the order in which the countries are displayed"
                  onChange={setRankingOrder}
                  defaultValue='DESC'
                >
                  <Group mt="xs">
                    <Radio value="ASC" label="↑"/>
                    <Radio value="DESC" label="↓"/>
                  </Group>
                </Radio.Group>
                <Divider my="sm"/>
                <Space h='lg' />
                <Text >Number of Countries</Text>
                <Space h='sm' />
                <Slider
                  marks={[
                    { value: 0, label: '' },
                    { value: 10, label: '10' },
                    { value: 20, label: '20' },
                    { value: 30, label: '30' },
                    { value: 40, label: '40' },
                    { value: 50, label: '' },
                  ]}
                  onChange={setRankingBatchNum}
                  max={50}
                  style={{ margin: 6 }}
                />
              </Flex>
            </>}
          </Drawer>
          <Space w='md' style={{ flex: 4 }}/>
          <Container>
            <Dropdown
              placeholder='Search country'
              style={{ width: 400 }}
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
          <Space w='md'  style={{ flex: 6 }}/>
          <Container size='xl'>
            {username == null ?
              <Flex justify='space-around'>
                <Button onClick={() => setDrawerTitle('Sign Up')}>Sign Up</Button>
                <Space w='sm' />
                <Button onClick={() => setDrawerTitle('Login')}>Login</Button>
              </Flex> :
              <ActionIcon><Avatar onClick={() => setDrawerTitle(`${username}'s Profile`)} src={null} alt={username} color='red'>{username[0]?.toLocaleUpperCase()}</Avatar></ActionIcon>}
          </Container>
          <Modal size={500} opened={drawerTitle !== null} onClose={() => setDrawerTitle(null)} title={drawerTitle}>
              {drawerTitle === 'Sign Up' && <SignUp setUsername={username => {
                setUsername(username);
                setDrawerTitle(`${username}'s Profile`);
              }} />}
              {drawerTitle === 'Login' && <Login setUsername={username => {
                setUsername(username);
                setDrawerTitle(`${username}'s Profile`);
              }} />}
              {username != null && drawerTitle === `${username}'s Profile` && <UserProfile username={username} logout={() => {
                setUsername(null);
                setDrawerTitle(null);
              }} />}
              {drawerTitle === 'Game' && username !== null && <Game username={username} />}
          </Modal>
      </Flex>

      <MapChart
        setTooltipStats={setTooltipStats}
        setCountryStats={setCountryStats}
        countryStats={countryStats}
      />

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
