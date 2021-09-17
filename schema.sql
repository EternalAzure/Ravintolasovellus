CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    created_at TIMESTAMP, 
    address TEXT
);

CREATE TABLE review_categories (
    id SERIAL PRIMARY KEY,
    category TEXT
);

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    grade INTEGER,
    restaurant_id INTEGER REFERENCES restaurants,
    category_id INTEGER REFERENCES review_categories
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP,
    restaurant_id INTEGER REFERENCES restaurants
);