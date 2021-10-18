from flask import request, session, flash, redirect
import db, json, collections
import map, search
from math import inf

# Small miscelanious functions

def sorted_restaurants():
    city = "Helsinki"
    if "city" in session:
        city = session["city"]

    restaurants = db.select_restaurants_limited(city)
    list = [None] * len(restaurants)
    i = 0
    for r in restaurants:
        list[i] = {
            "name": r.name, 
            "rating": db.grades_full_summary(r.id), 
            "created_at": r.created_at, 
            "id": r.id, 
            "city": r.city, 
            "street": r.street
            }
        i += 1

    list.sort(key=sort_by_rating)
    return list


def sort_by_rating(e):
    # Descending
    try:
        return 0 - e["rating"]
    except:
        return inf

# Fails if not all review categories are rated/graded
def insert_grades(restaurant_id):
    print("Utils")
    categories = db.categories()
    list = []
    # List of tuples [(category, grade), ...]
    try:
        list = [(request.form[str(c.id)], c.id) for c in categories]
    except:
        flash("Arvostele kaikki kategoriat")
        return redirect(f"/review/{restaurant_id}#one")

    try:
        user = session["user_id"]
        logged_in_grading(user, list, restaurant_id)
    except KeyError:
        print("userless")
        for tuple in list:
            db.insert_grade_userless(tuple[0], tuple[1], restaurant_id)
    return redirect(f"/review/{restaurant_id}#one")

def logged_in_grading(user, grades, restaurant):
    print("logged in grade")
    if db.has_graded(user, restaurant):
        for grade in grades:
            db.update_grade(grade[0], grade[1], user, restaurant)
    else:
        for grade in grades:
            db.insert_grade(grade[0], grade[1], user, restaurant)

def json_restaurants():
    # Convert query to objects of key-value pairs
    city = "Helsinki"
    if "city" in session:
        city = session["city"]
    rows = None
    rows = db.select_restaurants_limited(city)

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["street"] = row[2]
        d["city"] = row[3]
        d["created_at"] = str(row[4])
        d["location"] = map.location(row["city"], row["street"])
        objects_list.append(d)
    
    j = json.dumps(objects_list)
    return j

def json_location():
    city = "Helsinki"
    if "city" in session:
        city = session["city"]
    location =map.location(city, "")
    j = json.dumps(location)
    return j

