-- create temporary tables to import from csv
CREATE TEMPORARY TABLE Countries_in(
    name VARCHAR(60),
    slug VARCHAR(60),
    region_name VARCHAR(60)
);

CREATE TEMPORARY TABLE Iso_in(
    name VARCHAR(60),
    iso CHAR(3)
);


-- populate temporary tables with csv data
COPY Countries_in
FROM %s 
WITH (FORMAT CSV, HEADER TRUE);

COPY Iso_in
FROM %s
WITH (FORMAT CSV, HEADER TRUE);


-- populate Region
INSERT INTO Region (name)
SELECT DISTINCT region_name
FROM Countries_in;


-- populate Country
INSERT INTO Country (id, name, region_id)
SELECT Iso_in.iso, Iso_in.name, Region.id
FROM Countries_in
JOIN Iso_in ON Countries_in.name=Iso_in.name
JOIN Region ON Region.name=Countries_in.region_name;


-- drop temporary tables
DROP TABLE Countries_in;
DROP TABLE Iso_in;
