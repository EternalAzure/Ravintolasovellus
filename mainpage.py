from flask import render_template
import db
import sys
from math import inf

def render():
    #restaurants = db.restaurants()
    #restaurants.sort(key=sortByGrade)

    dictionaries = zipper()
    return render_template("index.html", dictionaries=dictionaries)


def sort_by_grade(e):
    #Descending
    try:
        return 0 - db.rating(e.id)
    except:
        return inf

def zipper():
    restaurants = db.restaurants()
    list = [None] * len(restaurants)
    i = 0
    for r in restaurants:
        list[i] = {"name": r.name, "rating": db.rating(r.id), "created_at": r.created_at, "id": r.id}
        i += 1
    log(list)
    #Sort list here
    return list

def log(output):
    print("log:"+ str(output), file=sys.stdout)
