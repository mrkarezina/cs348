select value from population where country_id='USA';
select value from area where country_id='CAN';
select value from gini_index where country_id='CHN';
select value from education_expenditure where country_id='KOR';

SELECT country_id, value FROM area ORDER BY value asc LIMIT 10;

SELECT country_id, value FROM gini_index ORDER BY value desc LIMIT 12;

SELECT country_id, value FROM area ORDER BY value desc LIMIT 3;




































