import { TextInput, Button, Container, Avatar, Flex, Space, Table, Text, Divider } from '@mantine/core';
import { useState, useEffect } from 'react';
import { UserInfo, getUserInfo } from './apiCalls';

export default function UserProfile({ username, logout }: { username: string, logout: () => void }) {
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    useEffect(() => {
        getUserInfo(username).then(info => {
            setUserInfo(info)
        });
    }, []);

    const scores = userInfo?.scores?.map((score, idx, _) => {
        return (
            <tr key={idx}>
                <td>{idx + 1}</td>
                <td>{score}</td>
            </tr>
        )
    });

    
    return (
        <Flex direction="column" justify="flex_end">
            {scores?.length ?
                <>
                    <Table>
                        <thead>
                            <tr>
                                <th>Game</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>{scores}</tbody>
                    </Table>
                    <Divider my="sm" />
                </>
            : <></>}
            <Text>Number of games played: {scores?.length}</Text> 
            <Space h="xl" />
            <Button onClick={logout}>Logout</Button>
        </Flex>
    );
}