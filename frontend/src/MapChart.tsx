import React, { useEffect, useState } from 'react';
import {
    ComposableMap,
    Geographies,
    Geography,
    Sphere,
    Graticule
} from 'react-simple-maps';

const MapChart = ({ setTooltipContent }: { setTooltipContent: (name: string) => void }) => {

    return <div data-tooltip-id='map-tooltip'>
        <ComposableMap>
            <Geographies geography='/features.json'>
                {({ geographies }: { geographies: Array<Geography> }) =>
                    geographies.map((geo: Geography) => (
                        <Geography
                            key={geo.rsmKey}
                            geography={geo}
                            onMouseEnter={() => {
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
        </ComposableMap>
    </div>;
};

export default React.memo(MapChart);
