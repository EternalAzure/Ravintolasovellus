from app import app
from flask import render_template, request, redirect
import db
import mainpage
import utils
import update_info
import sys

def log(m):
    print("LOG: " + str(m), file=sys.stdout)

@app.route("/")
def index():
    return mainpage.render()

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    street = request.form["street"]
    city = request.form["city"]
    #Validate address
    #m.location(city, street)
    #
    #
    restaurant_id = db.insert_restaurant(name, street, city)
    db.insert_info_all(None, None, "", [], restaurant_id)
    return redirect("/")

@app.route("/review/<int:id>")
def review(id):
    name = db.select_restaurant(id).name
    categories = db.categories()
    return render_template("review.html", id=id, name=name, categories=categories)

@app.route("/result/<int:id>")
def result(id):
    name = db.select_restaurant(id).name
    text_reviews = db.select_reviews(id)
    general_grade = db.grades_full_summary(id)
    grades = db.grades_partial_summary(id)
    return render_template("result.html", name=name, general_grade=general_grade, grades=grades, reviews=text_reviews, id=id)

@app.route("/answer", methods=["POST"])
def answer():
    restaurant = request.form["id"]
    review =request.form["review"]
    db.insert_review(review, restaurant)
    utils.insert_grades(restaurant)
    return redirect("/result/" + str(restaurant))

@app.route("/restaurant/<int:id>", methods=["GET"])
def restaurant(id):
    data = db.select_restaurant(id)
    info = db.select_info_all(id)
    info = utils.stringify(info)
    log(info.tags)
    return render_template("restaurant.html.j2", data=data, info=info, id=id)   

@app.route("/delete_restaurant/<int:id>")
def delete_restaurant(id):
    db.delete_restaurant(id)
    return redirect("/")

@app.route("/delete_review/<int:id>", methods=["POST"])
def delete_review(id):
    log("DELETE_REVIEW")
    review_id = request.form["review_id"]
    log(review_id)
    db.delete_review(review_id)
    return redirect("/result/"+str(id))

@app.route("/api/restaurants", methods=["GET"])
def restaurants():
    return utils.json_restaurants()

@app.route("/update_info", methods=["POST"])
def update():
    opening = request.form["opening"]
    closing = request.form["closing"]
    description = request.form["description"]
    tag = request.form["tag"]
    id = request.form["id"]
    return update_info.handle_input(opening, closing, description, tag, id)