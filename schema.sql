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

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    grade INTEGER,
    restaurant_id INTEGER REFERENCES restaurants
    ON DELETE CASCADE,
    category_id INTEGER REFERENCES review_categories
    ON DELETE CASCADE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pwhash TEXT,
    role TEXT,
    city_id INTEGER REFERENCES cities
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