import React, { useEffect, useState } from 'react';
import {
    ComposableMap,
    Geographies,
    Geography,
    Sphere,
    Graticule
} from 'react-simple-maps';
import { IPosition } from 'react-tooltip';

const MapChart = ({ setTooltipContent, setTooltipPosition }: { setTooltipContent: (name: string) => void, setTooltipPosition: (position: IPosition) => void }) => {
    return <ComposableMap height={490} width={1000} data-tooltip-id='map-tooltip'>
            <Geographies geography='/features.json'>
                {({ geographies }: { geographies: Array<any> }) =>
                    geographies.map((geo: any) => (
                        <Geography
                            key={geo.rsmKey}
                            geography={geo}
                            onMouseEnter={e => {
                                setTooltipPosition({x: e.clientX, y: e.clientY});
                                setTooltipContent(geo.properties.name);
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

export default React.memo(MapChart);
