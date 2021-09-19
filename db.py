from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import sys

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


def restaurants():
    sql = "SELECT restaurants.id, name, created_at, city, street FROM addresses, restaurants, streets, cities " \
          "WHERE restaurants.address_id=addresses.id AND addresses.city_id=cities.id AND addresses.street_id=streets.id"
    result = db.session.execute(sql)
    return result.fetchall()

def restaurant(id):
    sql = "SELECT name FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def categories():
    sql = "SELECT id, category FROM review_categories"
    result = db.session.execute(sql)
    return result.fetchall()

def category(id):
    sql = "SELECT category FROM review_categories WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def get_street_id(street):
    log(street)
    sql = "SELECT id FROM streets WHERE street=:street"
    result = db.session.execute(sql, {"street": street})
    return result.fetchone()[0]

def get_city_id(city):
    log(city)
    sql = "SELECT id FROM cities WHERE city=:city"
    result = db.session.execute(sql, {"city": city})
    return result.fetchone()[0]

def reviews(id):
    sql = "SELECT id, content, sent_at FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def rating(id):
    sql = "SELECT 1.0*SUM(grade)/NULLIF(COUNT(grade), 0) AS average FROM grades " \
          "WHERE grades.restaurant_id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":id})
    
    try:
        value = result.fetchone()[0]
        return round(value,  1)
    except:
        return "None"

def get_grades(restaurant):
    sql = "SELECT r.category, ROUND(1.0*SUM(grade)/NULLIF(COUNT(grade), 0), 1) AS average FROM review_categories r LEFT JOIN grades " \
          "ON r.id=grades.category_id WHERE grades.restaurant_id=:restaurant GROUP BY r.category"
    result = db.session.execute(sql, {"restaurant": restaurant})
    return result 

def insert_restaurant(name, street, city):
    street_id = insert_street(street)
    city_id = insert_city(city)
    log(street_id)
    log(city_id)
    address_id = insert_address(street_id, city_id)
    log(address_id)

    sql = "INSERT INTO restaurants (name, address_id, created_at) VALUES (:name, :address_id, NOW()) RETURNING id"
    result = db.session.execute(sql, {"name":name, "address_id":address_id})
    db.session.commit()
    return result

def insert_address(s_id, c_id):
    sql = "INSERT INTO addresses (street_id, city_id) VALUES (:s_id, :c_id) RETURNING id"
    result = db.session.execute(sql, {"s_id":s_id, "c_id":c_id})
    db.session.commit()
    return result.fetchone()[0]

def insert_street(street):
    try:
        sql = "INSERT INTO streets (street) VALUES (:street) RETURNING id"
        result = db.session.execute(sql, {"street":street})
        db.session.commit()
        return result.fetchone()[0]
    except:
        db.session.commit()
        return get_street_id(street)
    
def insert_city(city):
    try:
        sql = "INSERT INTO cities (city) VALUES (:city) RETURNING id"
        result = db.session.execute(sql, {"city":city})
        db.session.commit()
        return result.fetchone()[0]
    except:
        db.session.commit()
        return get_city_id(city)
    
def insert_review(review, restaurant):
    if review == "": return
    sql = "INSERT INTO reviews (content, restaurant_id, sent_at) VALUES (:review, :restaurant, NOW())"
    db.session.execute(sql, {"review":review, "restaurant":restaurant})
    db.session.commit()

def insert_grade(grade, restaurant, category):
    sql = "INSERT INTO grades (grade, restaurant_id, category_id) VALUES (:grade, :r_id, :c_id)"
    db.session.execute(sql, {"grade":grade, "r_id":restaurant, "c_id":category})
    db.session.commit()

def delete(id):
    sql = "DELETE FROM restaurants WHERE id=:id"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    
def log(m):
    print("LOG: " + str(m), file=sys.stdout)