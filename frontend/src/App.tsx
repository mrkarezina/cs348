import { useState } from 'react';
import { Tooltip } from 'react-tooltip';
import 'react-tooltip/dist/react-tooltip.css';
import 'semantic-ui-css/semantic.min.css';
import { Dropdown } from 'semantic-ui-react';
import { CountryStats, fetchCountryInfo } from './apiCalls';
import MapChart from './MapChart';
import { ThemeProvider } from './ThemeProvider';
import { countryOptions } from './Countries';
import { Container, Drawer, Button, Group, Flex, Center, Space } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { TextInput } from '@mantine/core';
import { IconAt } from '@tabler/icons-react';
import LoginSignUp from './LoginSignUp';
import UserProfile from './UserProfile';
import Game from './Game';
import { useCookie } from './utils';
import { Avatar, ActionIcon, Box } from '@mantine/core';
import { IconStar } from '@tabler/icons-react';

export default function App() {
  const [tooltipStats, setTooltipStats] = useState<CountryStats | null>(null);
  const [countryStats, setCountryStats] = useState<CountryStats | null>(null);

  const [username, setUsername] = useCookie('username', null);

  const [opened, { open, close }] = useDisclosure(false);
  const [drawerTitle, setDrawerTitle] = useState<string | null>(null);

  return <>
    <ThemeProvider>

      {/* top bar */}
      <Flex justify={"flex-end"} style={{ marginTop: 8 }}>
          <Space w="md"  style={{ flex: 7.5 }}/>
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
          <Space w="md"  style={{ flex: 6 }}/>
          <Container size='xl'>
            {username == null ? 
              <Button onClick={() => setDrawerTitle('Login / Sign up')}>Login / Sign up</Button> :
              <ActionIcon><Avatar onClick={() => setDrawerTitle('Profile')} src={null} alt={username} color='red'>{username[0]?.toLocaleUpperCase()}</Avatar></ActionIcon>}
          </Container>
          <Drawer size='md' position='right' opened={drawerTitle !== null} onClose={() => setDrawerTitle(null)} title={drawerTitle}>
            <Box maw={300} mx='auto'>
              {drawerTitle === 'Login / Sign up' && <LoginSignUp setUsername={username => {
                setUsername(username);
                setDrawerTitle('Scores');
              }} />}

              {drawerTitle === 'Profile' && <UserProfile logout={() => {
                setUsername(username);
                setDrawerTitle(null);
              }} />}

              {drawerTitle === 'Game' && <Game />}
            </Box>
          </Drawer>
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
