import { TextInput } from '@mantine/core';
import { IconAt } from '@tabler/icons-react';

export default function Game() {
    return <>
        <TextInput label='Your email' placeholder='Your email' icon={<IconAt size='0.8rem' />} />
    </>;
}