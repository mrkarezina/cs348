import { ActionIcon, Avatar, Button, Container, Drawer, Flex, Modal, Slider, Space, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import 'semantic-ui-css/semantic.min.css';
import { Dropdown } from 'semantic-ui-react';
import { CountryStats, fetchCountryInfo, getLeaderboard } from './apiCalls';
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
  {key: 'area', value: 'area', text: 'Area'},
  {key: 'education_expenditure', value: 'education_expenditure', text: 'Education expenditure'},
  {key: 'gini_index', value: 'gini_index', text: 'Gini index'},
  {key: 'population', value: 'population', text: 'Population'},
  {key: 'real_gdp', value: 'real_gdp', text: 'GDP'},
  {key: 'unemployment_rate', value: 'unemployment_rate', text: 'Unemployment rate'},
]

export default function App() {
  const [tooltipStats, setTooltipStats] = useState<CountryStats | null>(null);
  const [countryStats, setCountryStats] = useState<CountryStats | null>(null);
  const [rankingStat, setRankingStat] = useState<string | null>(null);

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
              <Flex direction={'column'}>
                <Dropdown
                  placeholder='Area'
                  style={{ width: 20 }}
                  selection
                  onChange={async (event, data) => {
                    setRankingStat(data.name);
                  }}
                  text={rankingStat!}
                  options={stats}
                />
                <Space h='lg' />
                <Text>Number of Countries</Text>
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
                  max={50}
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
