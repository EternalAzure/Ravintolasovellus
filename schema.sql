DROP TABLE IF EXISTS streets CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS addresses CASCADE;
DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS review_categories CASCADE;
DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS info CASCADE;
DROP TABLE IF EXISTS images CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS tag_relations CASCADE;

CREATE TABLE streets (
    id SERIAL PRIMARY KEY,
    street TEXT UNIQUE
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city TEXT UNIQUE
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    street_id INTEGER 
    REFERENCES streets
    ON DELETE CASCADE,
    city_id INTEGER 
    REFERENCES cities
    ON DELETE CASCADE
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    created_at TIMESTAMP, 
    address_id INTEGER REFERENCES addresses
);

CREATE TABLE review_categories (
    id SERIAL PRIMARY KEY,
    category TEXT UNIQUE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pwhash TEXT,
    role TEXT,
    city_id INTEGER REFERENCES cities
);

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    grade INTEGER,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE,
    category_id INTEGER REFERENCES review_categories
    ON DELETE CASCADE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE,
    user_id INTEGER REFERENCES users
);


CREATE TABLE info (
    id SERIAL PRIMARY KEY,
    descript TEXT,
    service_hours TEXT[],
    homepage TEXT,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE
);


CREATE TABLE images (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    data BYTEA, 
    r_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE
);


CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tag TEXT UNIQUE
);

CREATE TABLE tag_relations (
    id SERIAL PRIMARY KEY,
    tag_id INTEGER REFERENCES tags
    ON DELETE CASCADE,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE
);

INSERT INTO review_categories (category) VALUES ('viihtyisyys');
INSERT INTO review_categories (category) VALUES ('hinta-laatu');
INSERT INTO review_categories (category) VALUES ('maukkaus');

INSERT INTO cities (city) VALUES ('Helsinki');
INSERT INTO cities (city) VALUES ('Espoo');
INSERT INTO cities (city) VALUES ('Vantaa');
INSERT INTO cities (city) VALUES ('Tampere');
INSERT INTO cities (city) VALUES ('Turku');

INSERT INTO users (username, role, city_id, pwhash) 
VALUES ('admin', 'admin', 1, 'pbkdf2:sha256:260000$MMNEnyTqOOjjKUGU$9e66952f9173770520035efec9d269f71e1e8dca9a3735d961db35a3569df5c3');