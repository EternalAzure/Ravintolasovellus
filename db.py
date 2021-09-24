from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from os import getenv
import sys
from werkzeug.security import check_password_hash, generate_password_hash
from flask import make_response, session as browsing_session

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

#IMAGES
def select_image(id):
    sql = "SELECT data FROM images WHERE r_id=:id"
    result = db.session.execute(sql, {"id":id})
    try:
        data = result.fetchone()[0]
        response = make_response(bytes(data))
        response.headers.set("Content-Type", "image/jpeg")
        return response
    except TypeError:
        return None

def insert_image(name, data, r_id):
    sql = "INSERT INTO images (name,data,r_id) VALUES (:name,:data,:r_id)"
    db.session.execute(sql, {"name":name, "data":data, "r_id":r_id})
    db.session.commit()

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
def select_restaurants_limited(city):
    sql =   "SELECT restaurants.id as id, name, street, city, created_at "\
            "FROM "\
            "(SELECT "\
            "addresses.id as id, "\
            "addresses.street_id as street_id, "\
            "cities.city as city "\
            "FROM addresses, "\
            "(SELECT id, city FROM cities "\
            "WHERE city=:city) as cities "\
            "WHERE city_id=cities.id) as addresses, "\
            "streets, restaurants "\
            "WHERE addresses.street_id=streets.id "\
            "AND restaurants.address_id=addresses.id;"\
          
    result = db.session.execute(sql, {"city": city})
    return result.fetchall()

#Soon redundant??
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
    street_id = insert_street(street)
    city_id = insert_city(city)
    address_id = insert_address(street_id, city_id)

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
    user = browsing_session["user_id"] # alias session
    sql = "INSERT INTO reviews (content, restaurant_id, user_id, sent_at) VALUES (:review, :restaurant, :user, NOW())"
    db.session.execute(sql, {"review":review, "restaurant":restaurant, "user": user})
    db.session.commit()

def select_reviews(id):
    #
    #
    #Order by sent_at
    sql = "SELECT * FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def delete_review(id):
    log("DB DELETE_REVIEW("+str(id)+")")
    sql ="DELETE FROM reviews WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()


#USER TABLE
#----------------
def insert_user(username, password, role, city):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, pwhash, role, city) VALUES (:username, :pwhash, :role, :city)"
    db.session.execute(sql, {"username": username, "pwhash": hash_value, "role": role, "city": city})
    db.session.commit()

def verify_user(username, password):
    sql = "SELECT id, pwhash FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    

    if not user:
        return False
    else:
        hash_value = user.pwhash
        if check_password_hash(hash_value, password):
           return True
        else:
            return False

def is_username_taken(username):
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    row = result.fetchone()

    if row: return True
    return False

def select_users_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]

def select_users_role(username):
    sql = "SELECT role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]

def select_users_city(username):
    sql = "SELECT city FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()[0]

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

def is_info_ref(id):
    sql = "SELECT 1 FROM info WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    row = result.fetchone()
    if row: return True
    return False

def select_info_hours(id):
    sql = "SELECT service_hours FROM info WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    hours = result.fetchone()[0]
    default = [["",""]]*7
    if hours == None:
        return default
    return hours

def select_info_tags(id):
    log("DB SELECT_INFO_TAGS")
    sql = "SELECT tags FROM info WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id": id})
    tags_array = result.fetchone()[0]
    log(tags_array)
    if tags_array: return tags_array
    else: return []


def initiate_info(id):
    sql = "INSERT INTO info (restaurant_id) VALUES (:r)"
    db.session.execute(sql, {"r": id})
    db.session.commit()

def update_info_hours(input, id):
    sql = "UPDATE info SET service_hours=:input WHERE restaurant_id=:id"
    db.session.execute(sql, {"input": input, "id": id})
    db.session.commit()

def update_info_description(input, id):
    sql = "UPDATE info SET descript=:input WHERE restaurant_id=:id;"
    db.session.execute(sql, {"input": input, "id": id})
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