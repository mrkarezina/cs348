import { Box, TextInput, PasswordInput, Button, Group } from '@mantine/core';
import { IconUser } from '@tabler/icons-react';
import { useForm } from '@mantine/form';
import { Message, UserSignUpInfo, createNewUser } from './apiCalls';
import { showNotification } from '@mantine/notifications';

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
            .then(() => {
                showNotification({ title: `Signed up and logged in as ${user_signup_info.username}`, message: '' });
                setUsername(user_signup_info.username);
            }
            )
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

