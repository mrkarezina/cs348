-- create temporary tables to import from csv
CREATE TEMPORARY TABLE Stat_in(
    name VARCHAR(60),
    slug VARCHAR(60),
    value VARCHAR(60),
    date VARCHAR(60),
    ranking VARCHAR(60),
    region_name VARCHAR(60)
);

-- populate temporary table with csv data
COPY Stat_in (name, slug, value, date, ranking, region_name)
FROM '{csv}'
WITH (FORMAT CSV, HEADER TRUE);

-- populate stat table
INSERT INTO {table_name} (date_of_info, country_id, value)
SELECT
    CASE
        WHEN Stat_in.date!='' THEN CAST (LEFT(regexp_replace(Stat_in.date, '[^0-9]+', ''), 4) AS INTEGER)
        ELSE date_part('year', (SELECT current_timestamp))
    END,
    Country.id,
    CAST(TRANSLATE(Stat_in.value, ',$', '') AS FLOAT)
FROM Stat_in
JOIN Country ON Country.name=Stat_in.name;

-- drop temporary tables
DROP TABLE Stat_in;
