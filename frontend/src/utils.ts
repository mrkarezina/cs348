import { useState, useEffect, Dispatch, SetStateAction } from 'react';
import Cookies from 'js-cookie';

export function useCookie(key: string, defaultValue: string | null = null, { expires = 365000, sameSite = 'lax', path = '/' } = {}): [string | null, Dispatch<SetStateAction<string | null>>] {
    // cookie expires in a millenia
    // sameSite != 'strict' because the cookie is not read for sensitive actions
    // synchronous
    const cookieValue = Cookies.get(key);
    const [state, setState] = useState<string | null>(cookieValue || defaultValue);
    useEffect(() => {
        if (state === null || state == undefined) {
            Cookies.remove(key);
        } else {
            Cookies.set(key, state, { expires, sameSite: 'lax', path });
        }
    }, [state]);
    return [state, setState];
}