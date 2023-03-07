import { countriesMap } from './Countries';

const COUNTRY_OVERVIEW_URL = 'http://localhost:5001/api/country-overview?country_id=';

export interface CountryStats {
    code: string,
    name: string;
    population: number;
    area: number;
    giniIndex: number;
    gdp: number;
    unemployment_rate: number;
    education_epd: number;
}

export const fetchCountryInfo = async ({ code }: { code: string }): Promise<CountryStats> => {
    const info = await fetch(`${COUNTRY_OVERVIEW_URL}${code}`, { cache: 'force-cache' }).then(res => res.json()).then(data => data);
    return {
        code,
        name: countriesMap[code.toLowerCase()],
        population: info[`${code}`].population,
        area: info[`${code}`].area,
        giniIndex: info[`${code}`].gini_index,
        gdp: info[`${code}`].gdp,
        unemployment_rate: info[`${code}`].unemployment_rate,
        education_epd: info[`${code}`].education_expenditure,
    };
};
