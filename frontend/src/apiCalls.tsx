const COUNTRY_OVERVIEW_URL = 'http://localhost:5001/api/country-overview?country_id=';

export interface CountryStats {
    code: string,
    name: string;
    population: number;
    capital: string;
    giniIndex: number;
}

export const fetchCountryInfo = async ({ code }: { code: string }): Promise<CountryStats> => {
    const info = await fetch(`${COUNTRY_OVERVIEW_URL}${code}`, { cache: 'force-cache' }).then(res => res.json()).then(data => data);
    return {
        code: info.alpha3Code,
        name: info.name,
        population: info.population,
        capital: info.capital,
        giniIndex: info.gini,
    };
};
