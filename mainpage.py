from flask import render_template, session
from os import getenv
from math import inf
import db

def render():
    #url for map API with secret api key
    url = getenv("MAP")
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

    return render_template("index.html.j2", url=url, restaurants=list)

def sort_by_rating(e):
    #Descending
    try:
        return 0 - e["rating"]
    except:
        return inf
