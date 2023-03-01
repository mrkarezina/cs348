-- Table for Region
CREATE TABLE Region(
    id SERIAL,
    name VARCHAR(60) NOT NULL,
    PRIMARY KEY (id)
);

-- Table for Country
CREATE TABLE Country(
    id CHAR(3), -- using ISO 3166 standard
    name VARCHAR(60) NOT NULL,
    region_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (region_id) REFERENCES Region
        ON DELETE SET NULL 
);


-- Table for statistic: Area
CREATE TABLE Area(
    date_of_info INTEGER,
    country_id CHAR(3),
    value FLOAT CHECK (value > 0),
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

-- Table for statistic: GDP
CREATE TABLE GDP(
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

-- Table for Users
CREATE TABLE Users(
    user_id UUID,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_id)
);

-- Table for Games
CREATE TABLE Games(
    id SERIAL,
    user_id UUID,
    score INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users
        ON DELETE CASCADE
);


