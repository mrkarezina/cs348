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
}) => <ComposableMap height={490} width={1000}>
            <Geographies geography='./countries-50m.json'>
                {({ geographies }: { geographies: Array<any> }) =>
                    geographies.map((geo: any) => (
                        <Geography
                            key={geo.rsmKey}
                            data-tooltip-id='map-tooltip'
                            geography={geo}
                            onMouseEnter={async () => {
                                const infoObj = await fetchCountryInfo({ code: geo.id });
                                if (infoObj !== undefined) {
                                    setTooltipStats({
                                        code: geo.id,
                                        name: infoObj.name,
                                        area: infoObj.area,
                                        population: infoObj.population,
                                        giniIndex: infoObj.giniIndex,
                                        gdp: infoObj.gdp,
                                        unemployment_rate: infoObj.unemployment_rate,
                                        education_epd: infoObj.education_epd,
                                    });
                                } else {
                                    setTooltipStats({
                                        code: geo.id,
                                        name: geo.properties.name,
                                        area: 0,
                                        population: 0,
                                        giniIndex: 0,
                                        gdp: 0,
                                        unemployment_rate: 0,
                                        education_epd: 0,
                                    });
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
                                    setCountryStats({
                                        code: geo.id,
                                        name: infoObj.name,
                                        area: infoObj.area,
                                        population: infoObj.population,
                                        giniIndex: infoObj.giniIndex,
                                        gdp: infoObj.gdp,
                                        unemployment_rate: infoObj.unemployment_rate,
                                        education_epd: infoObj.education_epd,
                                    });
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
