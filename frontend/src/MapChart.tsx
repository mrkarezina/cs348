import React, { useEffect, useState } from 'react';
import {
    ComposableMap,
    Geographies,
    Geography,
    Sphere,
    Graticule
} from 'react-simple-maps';
import { IPosition } from 'react-tooltip';
import { CountryStats } from './App';

const MapChart = ({ setTooltipContent, setTooltipPosition, setCountryStats }: {
    setTooltipContent: (name: string) => void,
    setTooltipPosition: (position: IPosition) => void,
    setCountryStats: (stats: CountryStats) => void,
}) => {
    return <ComposableMap height={490} width={1000} data-tooltip-id='map-tooltip'>
            <Geographies geography='/features.json'>
                {({ geographies }: { geographies: Array<any> }) =>
                    geographies.map((geo: any) => (
                        <Geography
                            key={geo.rsmKey}
                            geography={geo}
                            onMouseEnter={async e => {
                                const info = await fetch_country_info({name: geo.properties.name});
                                const info_object = info[0];
                                setTooltipPosition({x: e.clientX, y: e.clientY});
                                setCountryStats({ name:info_object.name, capital:info_object.capital, population:info_object.population, gini_index:info_object.gini })
                            }}
                            onMouseLeave={() => {
                                setTooltipContent('');
                            }}
                            style={{
                                default: {
                                    fill: "#D6D6DA",
                                    outline: "none"
                                },
                                hover: {
                                    fill: "#F53",
                                    outline: "none"
                                },
                                pressed: {
                                    fill: "#E42",
                                    outline: "none"
                                }
                            }}
                        />
                    ))
                }
            </Geographies>
        </ComposableMap>;
};


const fetch_country_info = async ({ name }: { name: string }): Promise<string> => {
    const info = await fetch(`https://restcountries.com/v2/name/${name}`).then(res => res.json()).then(data => data);
    return info;
};

export default React.memo(MapChart);
