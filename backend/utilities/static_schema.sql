CREATE EXTENSION pgcrypto;

-- Table for Region
CREATE TABLE Region(
    id SERIAL,
    name VARCHAR(60) NOT NULL,
    PRIMARY KEY (id)
);

-- Table for Country
CREATE TABLE Country(
    id CHAR(3), -- using ISO 3166 alpha-3 code
    name VARCHAR(60) NOT NULL,
    region_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (region_id) REFERENCES Region
        ON DELETE SET NULL
);

-- Table for Users
CREATE TABLE Users(
    user_id UUID,
    username VARCHAR(50) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    PRIMARY KEY (user_id),
    CHECK (length(password) > 7)
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
