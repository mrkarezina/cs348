import { showNotification } from '@mantine/notifications';
import React from 'react';
import {
    ComposableMap,
    Geographies,
    Geography,
} from 'react-simple-maps';
import { CountryStats, fetchCountryInfo } from './apiCalls';

const MapChart = ({ setTooltipStats, setCountryStats, countryStats }: {
    setTooltipStats: (stats: CountryStats | null) => void,
    setCountryStats: (stats: CountryStats | null) => void,
    countryStats: CountryStats | null
}) => <ComposableMap height={490} width={1000} data-tooltip-id='map-tooltip'>
            <Geographies geography='/countries-50m.json'>
                {({ geographies }: { geographies: Array<any> }) =>
                    geographies.map((geo: any) => (
                        <Geography
                            key={geo.rsmKey}
                            geography={geo}
                            onMouseEnter={async () => {
                                const infoObj = await fetchCountryInfo({ code: geo.id });
                                if (infoObj !== undefined) {
                                    setTooltipStats({ code: geo.id, name: infoObj.name, capital: infoObj.capital, population: infoObj.population, giniIndex: infoObj.giniIndex });
                                } else {
                                    setTooltipStats({ code: geo.id, name: geo.properties.name, capital: 'Not found', population: 0, giniIndex: 0 });
                                    showNotification({ title: 'Error', message: `Could not find data on ${geo.properties.name}` });
                                }
                            }}
                            onMouseLeave={() => setTooltipStats(null)}
                            onMouseDown={async () => {
                                if (countryStats?.code === geo.id) {
                                    setCountryStats(null);
                                    return;
                                }
                                const infoObj = await fetchCountryInfo({ code: geo.id });
                                if (infoObj !== undefined) {
                                    setCountryStats({ code: geo.id, name: infoObj.name, capital: infoObj.capital, population: infoObj.population, giniIndex: infoObj.giniIndex });
                                } else {
                                    showNotification({ title: 'Error', message: `Could not set table for ${geo.properties.name} as no data could be found` });
                                }
                            }}
                            style={{
                                default: {
                                    fill: geo.id === countryStats?.code ? '#E42' : '#D6D6DA',
                                    outline: 'none',
                                },
                                hover: {
                                    fill: '#F53',
                                    outline: 'none',
                                },
                                pressed: {
                                    fill: '#E42',
                                    outline: 'none',
                                },
                            }}
                        />
                    ))
                }
            </Geographies>
    </ComposableMap>;

export default React.memo(MapChart);
