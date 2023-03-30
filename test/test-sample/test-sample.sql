SELECT value FROM population WHERE country_id='USA';

SELECT value FROM area WHERE country_id='CAN';

SELECT value FROM gini_index WHERE country_id='CHN';

SELECT value FROM education_expenditure WHERE country_id='KOR';

SELECT country_id, value FROM area ORDER BY value ASC LIMIT 10;

SELECT country_id, value FROM gini_index ORDER BY value DESC LIMIT 12;

SELECT country_id, value FROM area ORDER BY value DESC LIMIT 3;
