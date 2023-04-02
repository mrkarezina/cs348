import { Button, Group, PasswordInput, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { IconUser } from '@tabler/icons-react';
import { createNewUser, UserSignUpInfo } from './apiCalls';

export default function SignUp({ setUsername }: { setUsername: (username: string) => void }) {
    const form = useForm({
        initialValues: {
            username: '',
            password: '',
        },

        validate: {
            password: (value: string) => value.length > 7 ? null : 'Short password',
        },
    });

    const submitLoginSignUp = (user_signup_info: UserSignUpInfo) => {
        // make api call
        createNewUser(user_signup_info)
            .then(message => {
                if ('error' in message) throw message.error;
                showNotification({ title: `Signed up and logged in as ${user_signup_info.username}`, message: '' });
                setUsername(user_signup_info.username);
            })
            .catch(err => {
                console.error(err);
                showNotification({ title: 'ERROR: Could not login or signup', message: err, color: 'red' });
            });
    }

    return <>
        <form onSubmit={form.onSubmit(values => submitLoginSignUp(values))}>
            <TextInput withAsterisk label='Your username' placeholder='Your username' icon={<IconUser size='0.8rem' />} {...form.getInputProps('username')} />
            <PasswordInput label='Your password' placeholder='Your password' minLength={7} {...form.getInputProps('password')} />
            <Group position="right" mt="md">
                <Button type="submit">Sign Up</Button>
            </Group>
        </form>
    </>;
}
