import { Flex, Table } from '@mantine/core';
import { useEffect, useState } from 'react';
import { getLeaderboard } from './apiCalls';

export default function Leaderboard() {
    const [scoreRanking, setScoreRanking] = useState<[string, number][] | []>([]);
    useEffect(() => {
        getLeaderboard().then(rankings => setScoreRanking(rankings)).catch(console.error);
    }, []);

    const scores = scoreRanking?.map((user, idx, _) => {
        return (
            <tr key={idx}>
                <td>{idx + 1}</td>
                <td>{user[0]}</td>
                <td>{user[1]}</td>
            </tr>
        )
    });

    return (
        <Flex direction="column" justify="flex_end">
            {scores?.length ?
                <Table>
                    <thead>
                        <tr>
                            <th>Ranking</th>
                            <th>Username</th>
                            <th>Highest Score</th>
                        </tr>
                    </thead>
                    <tbody>{scores}</tbody>
                </Table>
            : <></>}
        </Flex>
    );
}
