from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import sys
import db

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
connection = SQLAlchemy(app)


@app.route("/")
def index():
    restaurants = db.restaurants(connection)
    restaurants.sort(key=sortByGrade)
    return render_template("index.html", restaurants=restaurants)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    address = request.form["address"]
    db.insertRestaurant(connection, name, address)
    return redirect("/")

@app.route("/review/<int:id>")
def review(id):
    name = db.restaurant(connection, id)
    categories = db.categories(connection)
    return render_template("review.html", id=id, name=name, categories=categories)

@app.route("/result/<int:id>")
def result(id):
    name = db.restaurant(connection, id)
    textReviews = db.reviews(connection, id)
    #calculates one average grade for all categories
    generalGrade = db.reviewTogether(connection, id)
    categories = db.categories(connection)
    gradesByCategory = []
    for c in categories:
        #calculates average grade by review category
        average = db.reviewSeparate(connection, id, c[0])
        gradesByCategory.append(average)
    return render_template("result.html", name=name, generalGrade=generalGrade, gradesByCategory=gradesByCategory, reviews=textReviews)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/answer", methods=["POST"])
def answer():
    restaurant = request.form["id"]
    review =request.form["review"]
    db.insertReview(connection, review, restaurant)
    categories = db.categories(connection)

    for c in categories:
        grade = request.form[str(c.id)]
        db.insertGrade(connection, grade, restaurant, c.id)

    return redirect("/result/" + str(restaurant))


def sortByGrade(e):
    #Descending
    try:
        return 0 - db.reviewTogether(connection, e.id)
    except:
        return 0

def log(output):
    print("log:"+ str(output), file=sys.stdout)
