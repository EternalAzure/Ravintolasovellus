from flask import render_template, session
from os import getenv
from math import inf
import sys

import map
import db

def render():
    log("MAINPAGE")
    N = 60.1699
    E = 24.9384
    #{"N": 60.1699, "E": 24.9384}
    restaurants = prepare()
    url = getenv("MAP")
    log("/MAINPAGE")
    return render_template("index.html.j2", url=url, N=(N), E=E, restaurants=restaurants)


def prepare():
    city = "Helsinki"
    if "city" in session:
        log("Has 'city field in session object'")
        city = session["city"]
        log(city)

    restaurants = db.select_restaurants_limited(city) 
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
        return 0 - e["rating"]
    except:
        return inf

def log(output):
    print("log:"+ str(output), file=sys.stdout)