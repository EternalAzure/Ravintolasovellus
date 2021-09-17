from flask import render_template
import db
import sys
from math import inf

def render():
    dictionaries = prepare()
    return render_template("index.html", dictionaries=dictionaries)

def prepare():
    restaurants = db.restaurants()
    list = [None] * len(restaurants)
    i = 0
    for r in restaurants:
        list[i] = {"name": r.name, "rating": db.rating(r.id), "created_at": r.created_at, "id": r.id}
        i += 1
    list.sort(key=sort_by_rating)
    return list

def sort_by_rating(e):
    #Descending
    try:
        #log(e["rating"])
        return 0 - e["rating"]
    except:
        return inf

def log(output):
    print("log:"+ str(output), file=sys.stdout)
