from flask import request
import db
from math import inf

#Small miscelanious functions

#Fecthes average grade for every category separately and returns a list
def get_grades(id):
    categories = db.categories()
    grades = []
    for c in categories:
        average = db.get_grades(id, c[0])
        grades.append(average)
    return grades

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
