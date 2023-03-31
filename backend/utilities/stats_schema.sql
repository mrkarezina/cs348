-- Table for statistic: Area
CREATE TABLE Area(
    date_of_info INTEGER,
    country_id CHAR(3),
    value INTEGER CHECK (value >= 0),
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
);

-- Table for statistic: Population
CREATE TABLE Population(
    date_of_info INTEGER,
    country_id CHAR(3),
    value FLOAT CHECK (value >= 0),
    pop_growth_rate FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
);

-- Table for statistic: Gini Index
CREATE TABLE Gini_Index(
    date_of_info INTEGER,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
);

-- Table for statistic: Real_GDP
CREATE TABLE Real_GDP(
    date_of_info INTEGER,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
);

-- Table for statistic: Unemployment Rate
CREATE TABLE Unemployment_Rate(
    date_of_info INTEGER,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
);

-- Table for statistic: Education Expenditure
CREATE TABLE Education_Expenditure(
    date_of_info INTEGER,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
);
