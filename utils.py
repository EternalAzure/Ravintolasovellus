from flask import request, session
import db
import json
import collections
import map
import sys
import re
import map

#
#Small miscelanious functions
#

#Goes through only if all review categories are rated/graded
def insert_grades(restaurant):
    categories = db.categories()
    final = [""] * len(categories)
    i = 0
    try:
        for c in categories:
            final[i] = (request.form[str(c.id)], c.id)
            i += 1
    except:
        log("exc")
        return

    for grade in final:
        db.insert_grade(grade[0], restaurant, grade[1])

def json_restaurants():
    # Convert query to objects of key-value pairs
    log("JSON_RESTAURANTS")
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
    log("/JSON_RESTAURANTS")
    return j

def json_location():
    log("/JSON_LOCATION")
    city = "Helsinki"
    if "city" in session:
        city = session["city"]
    location =map.location(city, "")
    j = json.dumps(location)
    log("/JSON_LOCATION")
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