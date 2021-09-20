from flask import render_template
from os import getenv
from math import inf
import sys
import map
import db
import json

def render():
    N = 60.1699
    E = 24.9384
    description = "Ravintola"
    #{"N": 60.1699, "E": 24.9384}
    restaurants = prepare()
    url = getenv("MAP")
    return render_template("index.html.j2", url=url, N=(N), E=E, restaurants=restaurants)


def prepare():
    restaurants = db.select_restaurants_all()
    list = [None] * len(restaurants)
    i = 0
    for r in restaurants:
        list[i] = {
            "name": r.name, 
            "rating": db.grades_full_summary(r.id), 
            "created_at": r.created_at, 
            "id": r.id, "city": r.city, 
            "street": r.street,
            "location": map.location(r.city, r.street)
            }
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