from flask import request, session
import db, json, collections
import map, sys, re, map
from math import inf

#Small miscelanious functions

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
            "id": r.id, "city": r.city, 
            "street": r.street
            }
        i += 1

    list.sort(key=sort_by_rating)
    return list


def sort_by_rating(e):
    #Descending
    try:
        return 0 - e["rating"]
    except:
        return inf

#Goes through only if all review categories are rated/graded
def insert_grades(restaurant):
    user = session["user_id"]
    categories = db.categories()
    final = [""] * len(categories)
    i = 0
    try:
        for c in categories:
            final[i] = (request.form[str(c.id)], c.id)
            i += 1
    except:
        return

    if db.is_grade(user):
        for grade in final:
            db.update_grade(grade[0], user, restaurant, grade[1])

    for grade in final:
        db.insert_grade(grade[0], user, restaurant, grade[1])

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
        log(d)
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

def firts_letter_capital(word):
    regex = "\\b[A-Z].*?\\b"
    format = re.compile(regex)  
    r = re.search(format, word)

    if r is None :
        return False
       
    else :
        return True

def log(output):
    print("log:"+ str(output), file=sys.stdout)