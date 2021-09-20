from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from os import getenv
import sys

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

#CATEGORIES TABLE
#----------------
def categories():
    sql = "SELECT id, category FROM review_categories"
    result = db.session.execute(sql)
    return result.fetchall()

def category(id):
    sql = "SELECT category FROM review_categories WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

#RESTAURANT TABLE & *
#----------------
def select_restaurants_all():
    sql = "SELECT restaurants.id, name, created_at, city, street FROM addresses, restaurants, streets, cities " \
          "WHERE restaurants.address_id=addresses.id AND addresses.city_id=cities.id AND addresses.street_id=streets.id"
    result = db.session.execute(sql)
    return result.fetchall()

def select_restaurant(id):
    sql = "SELECT restaurants.id, name, created_at, city, street FROM addresses, restaurants, streets, cities " \
          "WHERE restaurants.address_id=addresses.id AND addresses.city_id=cities.id AND addresses.street_id=streets.id " \
          "AND restaurants.id=:id"
    result = db.session.execute(sql, {"id":id})
    restaurant = result.fetchone()# <-- don't put that [0] there
    return restaurant

def delete_restaurant(id):
    sql = "DELETE FROM restaurants WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()

#Inserting restaurant is dependent on inserting street, city and address
def insert_restaurant(name, street, city):
    log("FUNCTION")
    street_id = insert_street(street)
    log(street_id)
    city_id = insert_city(city)
    log(city_id)
    address_id = insert_address(street_id, city_id)
    log(address_id)

    sql = "INSERT INTO restaurants (name, address_id, created_at) VALUES (:name, :address_id, NOW()) RETURNING id"
    result = db.session.execute(sql, {"name":name, "address_id":address_id})
    db.session.commit() #Transaction ends
    new_id = result.fetchone()[0]
    return new_id

def insert_address(s_id, c_id): #INSERT ADDRESS
    sql = "INSERT INTO addresses (street_id, city_id) VALUES (:s_id, :c_id) RETURNING id"
    result = db.session.execute(sql, {"s_id":s_id, "c_id":c_id})
    db.session.commit()
    return result.fetchone()[0]

def insert_street(street): #INSERT STREET
    try:
        sql = "INSERT INTO streets (street) VALUES (:street) RETURNING id"
        result = db.session.execute(sql, {"street":street})
        db.session.commit()
        return result.fetchone()[0]
    except exc.IntegrityError:
        db.session.commit()
        return get_street_id(street)
    
def insert_city(city): #INSERT CITY
    try:
        sql = "INSERT INTO cities (city) VALUES (:city) RETURNING id"
        result = db.session.execute(sql, {"city":city})
        db.session.commit()
        return result.fetchone()[0]
    except exc.IntegrityError:
        db.session.commit()
        return get_city_id(city)


#REVIEW TABLE
#----------------
def insert_review(review, restaurant):
    if review == "": return
    sql = "INSERT INTO reviews (content, restaurant_id, sent_at) VALUES (:review, :restaurant, NOW())"
    db.session.execute(sql, {"review":review, "restaurant":restaurant})
    db.session.commit()

def reviews(id):
    sql = "SELECT id, content, sent_at FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def delete_review(id):
    sql ="DELETE FROM reviews WHERE restaurant_id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()


#USER TABLE
#----------------
def insert_user(username, pwhash, role):
    sql = "INSERT INTO users (user, pwhash, role) VALUES (:username, :pwhash, :role)"
    db.session.execute(sql, {"username": username, "pwhash": pwhash, "role": role})
    db.session.commit()



#GRADES TABLE
#----------------
def insert_grade(grade, restaurant, category):
    sql = "INSERT INTO grades (grade, restaurant_id, category_id) VALUES (:grade, :r_id, :c_id)"
    db.session.execute(sql, {"grade":grade, "r_id":restaurant, "c_id":category})
    db.session.commit()

def grades_full_summary(id):
    sql = "SELECT 1.0*SUM(grade)/NULLIF(COUNT(grade), 0) AS average FROM grades " \
          "WHERE grades.restaurant_id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":id})
    
    try:
        value = result.fetchone()[0]
        return round(value,  1)
    except:
        return "None"

def grades_partial_summary(restaurant):
    sql = "SELECT r.category, ROUND(1.0*SUM(grade)/NULLIF(COUNT(grade), 0), 1) AS average FROM review_categories r LEFT JOIN grades " \
          "ON r.id=grades.category_id WHERE grades.restaurant_id=:restaurant GROUP BY r.category"
    result = db.session.execute(sql, {"restaurant": restaurant})
    return result 

#INFO TABLE
#----------------
def select_info_all(id):
    sql = "SELECT * FROM info WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    try:
        row = result.fetchall()[0]
    except IndexError:
        row = None
    return row

def select_info_tags(id):
    sql = "SELECT tags FROM info WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id": id})
    tags_array = result.fetchone()[0]
    return tags_array

def insert_info_all(opening, closing, description, tags, id):
    sql = "INSERT INTO info (opening, closing, descript, tags, restaurant_id) VALUES (:o, :c, :d, :t, :r)"
    db.session.execute(sql, {"o": opening, "c": closing, "d": description, "t": tags, "r": id})
    db.session.commit()

def update_info_opening(input, id):
    sql = "UPDATE info SET opening=:input WHERE restaurant_id=:id"
    db.session.execute(sql, {"input": input, "id": id})
    db.session.commit()

def update_info_closing(input, id):
    sql = "UPDATE info SET closing=:input WHERE restaurant_id=:id"
    db.session.execute(sql, {"input": input, "id": id})
    db.session.commit()

def update_info_description(input, id):
    log("Call")
    sql = "UPDATE info SET descript=:input WHERE restaurant_id=:id;"
    res = db.session.execute(sql, {"input": input, "id": id})
    db.session.commit()

def update_info_tags(input, id):
    sql = "UPDATE info SET tags=:input WHERE restaurant_id=:id"
    db.session.execute(sql, {"input": input, "id": id})
    db.session.commit()

#Auxiliary for intenal use
def get_street_id(street):
    sql = "SELECT id FROM streets WHERE street=:street"
    result = db.session.execute(sql, {"street": street})
    return result.fetchone()[0]

def get_city_id(city):
    sql = "SELECT id FROM cities WHERE city=:city"
    result = db.session.execute(sql, {"city": city})
    return result.fetchone()[0]

def log(m):
    print("LOG: " + str(m), file=sys.stdout)