from flask import render_template, request, redirect
import db
from math import inf
import sys
import map

def render():
    N = 60.1699
    E = 24.9384
    description = "Ravintola"
    #{"N": 60.1699, "E": 24.9384}
    restaurants = prepare()
    return render_template("index.html", description=description, N=(N), E=E, restaurants=restaurants)


def prepare():
    restaurants = db.restaurants()
    list = [None] * len(restaurants)
    i = 0
    for r in restaurants:
        list[i] = {
            "name": r.name, 
            "rating": db.rating(r.id), 
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