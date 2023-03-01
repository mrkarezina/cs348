-- Table for Region
CREATE TABLE Region(
    id  INT AUTO_INCREMENT,
    name VARCHAR(60) NOT NULL,
    PRIMARY KEY (id)
)

-- Table for Country
CREATE TABLE Country(
    id CHAR(3), -- using ISO 3166 standard
    name VARCHAR(60) NOT NULL,
    region_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (region_id) REFERENCES Region
        ON DELETE SET NULL 
)


-- Table for statistic: Area
CREATE TABLE Area(
    date_of_info YEAR,
    country_id CHAR(3),
    value FLOAT CHECK (val > 0),
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
)

-- Table for statistic: Population
CREATE TABLE Population(
    date_of_info YEAR,
    country_id CHAR(3),
    value FLOAT CHECK (val >= 0),
    pop_growth_rate FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
)

-- Table for statistic: Gini Index
CREATE TABLE Gini_Index(
    date_of_info YEAR,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
)

-- Table for statistic: GDP
CREATE TABLE GDP(
    date_of_info YEAR,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
)


-- Table for statistic: Unemployment Rate
CREATE TABLE Unemployment_Rate(
    date_of_info YEAR,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
)


-- Table for statistic: Education Expenditure
CREATE TABLE Education_Expenditure(
    date_of_info YEAR,
    country_id CHAR(3),
    value FLOAT,
    PRIMARY KEY (date_of_info, country_id),
    FOREIGN KEY (country_id) REFERENCES Country
        ON DELETE CASCADE
)

-- Table for User
CREATE TABLE User(
    user_id VARCHAR(255),
    name VARCHAR(50) NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY (uid)
)

-- Table for Game
CREATE TABLE Game(
    id INT AUTO_INCREMENT,
    user_id VARCHAR(255),
    score INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES User
        ON DELETE CASCADE
)
