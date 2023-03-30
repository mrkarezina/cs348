-- First display all tables by running "\dt"

-- GET /api/country_rankings_by_stat
SELECT country_id, value FROM area ORDER BY value DESC LIMIT 10;

-- GET /api/country_stats
SELECT value FROM population WHERE country_id='CAN';
SELECT value FROM area WHERE country_id='CAN';
SELECT value FROM gini_index WHERE country_id='CAN';
SELECT value FROM education_expenditure WHERE country_id='CAN';

-- POST /api/create_user
INSERT INTO users (user_id, username, password) values ('7207b9e3-85cf-4694-9b8a-ecba576a4345', 'rachelli', 'password1234');
SELECT * FROM users;

-- POST /api/login_user
SELECT EXISTS (SELECT 1 FROM users WHERE username = 'rachell' AND password = 'password1234');

-- GET /api/game
SELECT country_id, value FROM (SELECT id FROM country ORDER BY RANDOM() LIMIT 5) AS random_countries JOIN (SELECT country_id, value, date_of_info FROM Area ORDER BY date_of_info DESC) AS areas ON random_countries.id = areas.country_id GROUP BY country_id, value, date_of_info ORDER BY RANDOM();

-- POST /api/game
INSERT INTO games (user_id, score) VALUES ((SELECT user_id FROM users WHERE username = 'rachell'), 100);

-- GET /api/get_user
SELECT score FROM games WHERE user_id = (SELECT user_id FROM users WHERE username = 'rachell');

-- GET /api/get_leaderboard
SELECT username, score FROM games JOIN users ON games.user_id = users.user_id ORDER BY score DESC LIMIT 10;