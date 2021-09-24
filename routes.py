from app import app
from flask import render_template, request, redirect, session, flash
import db
import mainpage
import utils
import update_info
import register as r
import login as l
from set_city import set_city as set_session_city
from os import getenv
import sys


# IMAGE
@app.route("/send", methods=["POST"])
def send():
    file = request.files["file"]
    name = file.filename
    r_id = request.form["restaurant_id"]
    if not name.endswith(".jpg"):
        flash('Kelvoton tiedostonimi. Käytä .jpg')
        return redirect(request.referrer)
    data = file.read()
    if len(data) > 200*1024:
        flash('Tiedosto saa olla enintään 204kt')
        return redirect(request.referrer)
    db.insert_image(name, data, r_id)
    flash("Kuva ladattiin onnistuneesti")
    return redirect(request.referrer)

@app.route("/show/<int:id>")
def show(id):
    image = db.select_image(id)
    if image:return image
    return "No image"
# /IMAGE

@app.route("/")
def index():
    return mainpage.render()

@app.route("/new")
def new():
    return render_template("new.html.j2")

@app.route("/restaurant/<int:id>", methods=["GET"])
def restaurant(id):
    log("ROUTE /RESTAURANT")
    data = db.select_restaurant(id)
    info = db.select_info_all(id)
    days = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    hours = db.select_info_hours(id)
    tags = db.select_info_tags(id)
    log(tags)
    return render_template("info.html.j2", data=data, tags=tags, info=info, days=days, hours=hours, id=id)

@app.route("/review/<int:id>")
def review(id):
    name = db.select_restaurant(id).name
    categories = db.categories()
    return render_template("review.html.j2", id=id, name=name, categories=categories)

@app.route("/result/<int:id>")
def result(id):
    log("ROUTE /RESULT/" + str(id))
    name = db.select_restaurant(id).name
    text_reviews = list(db.select_reviews(id))
    text_reviews.reverse()
    general_grade = db.grades_full_summary(id)
    grades = db.grades_partial_summary(id)
    return render_template("result.html.j2", name=name, general_grade=general_grade, grades=grades, reviews=text_reviews, id=id)

@app.route("/set_city", methods=["POST"])
def set_city():
    log("ROUTE /set_city")
    city = request.form["city"]
    log(city)
    set_session_city(city)
    return redirect("/")
      
@app.route("/login_page") 
def login_page():
    return render_template("login_page.html.j2")

@app.route("/register_page")
def register_page():
    return render_template("register_page.html.j2")

@app.route("/delete_restaurant/<int:id>")
def delete_restaurant(id):
    db.delete_restaurant(id)
    return redirect("/")

@app.route("/delete_review/<int:id>", methods=["POST"])
def delete_review(id):
    review_id = request.form["review_id"]
    db.delete_review(review_id)
    return redirect("/result/"+str(id))

@app.route("/api/restaurants", methods=["GET"])
def restaurants():
    return utils.json_restaurants()

@app.route("/update_info", methods=["POST"])
def update():
    log("ROUTE /update_info")
    days = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    hours = []
    for d in days:
        opening = request.form["opening_"+d]
        closing = request.form["closing_"+d]
        hours.append([opening, closing])
    description = request.form["description"]
    tag = request.form["tag"]
    id = request.form["id"]
    return update_info.handle_input(hours, description, tag, id)

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
    db.initiate_info(restaurant_id)
    return redirect("/")

@app.route("/answer", methods=["POST"])
def answer():
    log("ROUTE /answer")
    restaurant = request.form["id"]
    review = request.form["review"]
    db.insert_review(review, restaurant)
    utils.insert_grades(restaurant)
    return redirect("/result/" + str(restaurant))

@app.route("/register", methods=["POST"])
def register():
    return r.register_user()


@app.route("/login",methods=["POST"])
def login():
    return l.login()

@app.route("/logout")
def logout():
    delete = [key for key in session]
    for key in delete: del session[key]
    return redirect("/")

@app.route("/admin")
def admin():
    log("ROUTE /ADMIN")
    log(request.remote_addr)
    log(getenv("TRUSTED_IP"))
    if request.remote_addr == getenv("TRUSTED_IP"):
        return render_template("admin.html")
    redirect("/")

@app.route("/register_admin", methods=["POST"])
def register_admin():
    return r.register_admin()

def log(m):
    print("LOG: " + str(m), file=sys.stdout)