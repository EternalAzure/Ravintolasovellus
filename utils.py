from flask import request
import db
from math import inf
import json
import collections
import map
import sys

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
    rows = db.select_restaurants_all()

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

def log(output):
    print("log:"+ str(output), file=sys.stdout)