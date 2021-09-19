from flask import request
import db
from math import inf
import json
import collections
import map

#Small miscelanious functions

#Gets grades from html radio elements
#Goes through only if all review categories are rated/graded
def insert_grades(restaurant):
    categories = db.categories()
    buffer = [None] * len(categories)
    i = 0
    try:
        for c in categories:
            buffer[i] = (request.form[str(c.id)], c.id)
            i += 1
    except:
        return

    for grade in buffer:
        db.insert_grade(grade[0], restaurant, grade[1])

def json_restaurants():
    # Convert query to objects of key-value pairs
    rows = db.restaurants()

    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["created_at"] = str(row[2])
        d["city"] = row[3]
        d["street"] = row[4]
        d["location"] = map.location(row["city"], row["street"])
        objects_list.append(d)
    
    j = json.dumps(objects_list)
    return j