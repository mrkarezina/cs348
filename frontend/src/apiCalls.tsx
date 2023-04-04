import { countriesMap } from './Countries';

const BASE_API_URL = 'http://localhost:5001/api';
const COUNTRY_OVERVIEW_URL = `${BASE_API_URL}/country_stats?country_id=`;
const USER_SIGN_UP_URL = `${BASE_API_URL}/create_user`;
const USER_LOGIN_URL = `${BASE_API_URL}/login_user`;
const USER_INFO_URL = `${BASE_API_URL}/user_scores?username=`;
const LEADER_BOARD_URL = `${BASE_API_URL}/get_leaderboard`;
const GAME_URL = `${BASE_API_URL}/game`;
const GET_COUNTRIES_RANKING = `${BASE_API_URL}/country_rankings_by_stat?stat_name=`;

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

export interface FilterRankingInfo {
    statName: string;
    region_id: string | null;
    n: number | null;
    order: string | null;
}

export const fetchCountryInfo = async ({ code }: { code: string }): Promise<CountryStats> => {
    const info = await fetch(`${COUNTRY_OVERVIEW_URL}${code}`).then(res => res.json());
    return {
        code,
        name: countriesMap[code?.toLowerCase()],
        population: info[`${code}`].population,
        area: info[`${code}`].area,
        giniIndex: info[`${code}`].gini_index,
        gdp: info[`${code}`].real_gdp,
        unemployment_rate: info[`${code}`].unemployment_rate,
        education_epd: info[`${code}`].education_expenditure,
    };
};

export const createNewUser = async (user_signup_info: UserSignUpInfo): Promise<Message> => {
    const message = await fetch(USER_SIGN_UP_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user_signup_info)
    }).then(res => res.json());

    return message;
};

export const loginUser = async (user_signup_info: UserSignUpInfo): Promise<Message> => {
    const message = await fetch(USER_LOGIN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user_signup_info)
    }).then(res => res.json());
    return message;
};

// get score for the logged in user
export const getUserInfo = async (username: string): Promise<UserInfo> => {
    return await fetch(`${USER_INFO_URL}${username}`).then(res => res.json());
};

export const getLeaderboard = async (): Promise<[string, number][]> => {
    return await fetch(LEADER_BOARD_URL).then(res => res.json());
};

export const getGameQuestions = async (): Promise<Array<[string, number]>> => {
    return await fetch(GAME_URL).then(res => res.json());
};

export const submitScore = async (username: string, score: number): Promise<Record<string, string>> => {
    return await fetch(GAME_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username,
            score
        })
    }).then(res => res.json());
};

export const getCountryRankings = async (filterRankingInfo: FilterRankingInfo): Promise<Array<[string, number]>> => {
    return await fetch(`${GET_COUNTRIES_RANKING}${filterRankingInfo.statName}${filterRankingInfo.region_id ? '&region_id=' + filterRankingInfo.region_id : ''}${filterRankingInfo.n ? '&limit=' + filterRankingInfo.n : ''}${filterRankingInfo.order ? '&order_by=' + filterRankingInfo.order : ''}`)
        .then(res => res.json());
}
