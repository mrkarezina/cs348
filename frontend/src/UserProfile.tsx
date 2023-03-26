import { TextInput, Button } from '@mantine/core';
import { IconAt } from '@tabler/icons-react';
import { useState, useEffect } from 'react';

export default function UserProfile({ logout }: { logout: () => void }) {
    const [scores, setScores] = useState<Array<Number>>([]);
    useEffect(() => {

    }, []);
    
    return <>
        <Button onClick={logout}>Logout</Button>
        TODO: show scores
    </>;
}