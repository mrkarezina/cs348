import { countriesMap } from './Countries';

const BASE_API_URL = 'http://localhost:5001/api';
const COUNTRY_OVERVIEW_URL = `${BASE_API_URL}/country_stats?country_id=`;
const USER_SIGN_UP_URL = `${BASE_API_URL}/create-user`;
const USER_LOGIN_URL = `${BASE_API_URL}/login-user`;
const USER_INFO_URL = `${BASE_API_URL}/get-user?username=`;

export interface CountryStats {
    code: string;
    name: string;
    population: number;
    area: number;
    giniIndex: number;
    gdp: number;
    unemployment_rate: number;
    education_epd: number;
}

export interface UserSignUpInfo {
    username: string;
    password: string;
}

export interface Message {
    message: string;
}

export interface UserInfo {
    scores: string[];
}

export const fetchCountryInfo = async ({ code }: { code: string }): Promise<CountryStats> => {
    const info = await fetch(`${COUNTRY_OVERVIEW_URL}${code}`).then(res => res.json()).then(data => data);
    return {
        code,
        name: countriesMap[code.toLowerCase()],
        population: info[`${code}`].population,
        area: info[`${code}`].area,
        giniIndex: info[`${code}`].gini_index,
        gdp: info[`${code}`].gdp,
        unemployment_rate: info[`${code}`].unemployment_rate,
        education_epd: info[`${code}`].education_expenditure,
    };
};


export const createNewUser = async (user_signup_info: UserSignUpInfo): Promise<Message> => {
    const message = await fetch(USER_SIGN_UP_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(user_signup_info)
    }).then(res => res.json()).then(data => data);

    return {
        message
    }
}

export const LoginUser = async (user_signup_info: UserSignUpInfo): Promise<Message> => {
    const message = await fetch(USER_LOGIN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(user_signup_info)
    }).then(res => res.json()).then(data => data);

    return {
        message
    }
}

// get score for the logined user
export const getUserInfo = async (username: string): Promise<UserInfo> => {
    return await fetch(`${USER_INFO_URL}${username}`).then(res => res.json()).then(data => data);
}


