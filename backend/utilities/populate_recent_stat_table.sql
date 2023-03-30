-- populate stat table
INSERT INTO {table_name}_recent (date_of_info, country_id, value)
SELECT
    stat_table.date_of_info, stat_table.country_id, stat_table.value
FROM {table_name} as stat_table
JOIN (
    SELECT MAX(date_of_info) AS recent_date, country_id
    FROM {table_name}
    GROUP BY country_id
    
) AS recent
ON stat_table.country_id=recent.country_id AND stat_table.date_of_info=recent.recent_date;
