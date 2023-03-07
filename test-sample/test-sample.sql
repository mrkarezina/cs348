-- Test queries for milestone 1, corresponding outputs can be found in test-sample.out

SELECT value FROM population WHERE country_id='USA';

SELECT value FROM area WHERE country_id='CAN';

SELECT value FROM gini_index WHERE country_id='CHN';

SELECT value FROM education_expenditure WHERE country_id='KOR';

SELECT country_id, value FROM area ORDER BY value asc LIMIT 10;

SELECT country_id, value FROM gini_index ORDER BY value desc LIMIT 12;

SELECT country_id, value FROM area ORDER BY value desc LIMIT 3;
