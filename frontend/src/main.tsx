import { NotificationsProvider } from '@mantine/notifications';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <NotificationsProvider>
        <App />
    </NotificationsProvider>
);
