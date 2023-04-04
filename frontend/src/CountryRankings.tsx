import { Button, Divider, Flex, ScrollArea, Space, Table, Text } from '@mantine/core';
import { countriesMap } from './Countries';
import { useEffect, useState } from 'react';

export default function CountryRankings({ rankings }: { rankings: Array<[string, number]>}) {
    const [countryRankings, setCountryRankings] = useState<Array<[string, number]>>([]);
    useEffect(() => {
        setCountryRankings(rankings);
    }, []);

    let rank_idx = 0;
    const countryRows = rankings.map((country, _idx, _) => {
        if (!!countriesMap[country[0].toLocaleLowerCase()]) {
            rank_idx += 1;
            return (
                <tr key={rank_idx}>
                    <td>{rank_idx}</td>
                    <td>{countriesMap[country[0].toLocaleLowerCase()]}</td>
                    <td>{country[1]}</td>
                </tr>
            )
        }
    });


    return (
        <ScrollArea h={700}>
            <Flex direction="column" justify="flex_end">
                {countryRows ?
                    <>
                        <Table>
                            <thead>
                                <tr>
                                    <th>Ranking</th>
                                    <th>Country</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>{countryRows}</tbody>
                        </Table>
                        <Divider my="sm" />
                    </>
                : <></>}
            </Flex>
        </ScrollArea>
    );
}