export interface CountryStats {
    code: string,
    name: string;
    population: number;
    capital: string;
    giniIndex: number;
}

export const fetchCountryInfo = async ({ code }: { code: string }): Promise<CountryStats> => {
    const info = await fetch(`https://restcountries.com/v2/alpha/${code}`, { cache: 'force-cache' }).then(res => res.json()).then(data => data);
    return {
        code,
        name: info.name,
        population: info.population,
        capital: info.capital,
        giniIndex: info.gini_index,
    };
};
