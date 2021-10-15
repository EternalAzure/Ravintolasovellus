import json
from app import app
from flask_cors import CORS
from flask import render_template, request, redirect, session, flash
import utils, update_info, db
import register as r
import login as l
from set_city import set_city as set_session_city
from os import getenv

#Lets client request data from static/index.js through API
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#RESOURCES
#----------------
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

#WEB PAGES
#----------------
@app.route("/old")
def index():
    #url for map API with secret api key
    url = getenv("MAP")
    list = utils.sorted_restaurants()
    return render_template("index.html", url=url, restaurants=list)

@app.route("/")
def demo():
    url = getenv("MAP")
    list = utils.sorted_restaurants()
    return render_template("demo.html", url=url, restaurants=list)

@app.route("/refresh")
def refresh():
    # To avoid the tedious header by skipping to section #one
    # Calling /#one will not be routed to server causing reload
    # but just moves viewport on page
    return redirect("/#one")

@app.route("/review/<int:id>", methods=["GET", "POST"])
def demo_reviews(id):
    #GET
    if request.method == "GET":
        name = db.select_restaurant(id).name
        categories = db.categories()
        text_reviews = list(db.select_reviews(id))
        text_reviews.reverse()
        general_grade = db.grades_full_summary(id)
        grades = db.grades_partial_summary(id)
        return render_template("review.html", name=name, categories=categories, 
                                                    id=id, reviews=text_reviews, 
                                                    grade=general_grade, grades=grades)
    #POST
    review = request.form["review"]
    if review:
        # Only logged in are allowed to give verbal review
        if "user_id" in session:
            user = session["user_id"]
            db.insert_review(review, id, user)
            # show all reviews for logged in users
            return redirect(f"/review/{id}#one")

        # If there is verbal review but no logged in account
        # then session is expired
        flash("Istunto on vanhentunut")
        return redirect("/#one")

    # show all reviews for non logged in users
    return redirect(f"review/{id}#one")

@app.route("/grade/<int:id>", methods=["POST"])
def grade(id):
     # Anyone can grade a restaurant
    if not utils.insert_grades(id):
        flash("Arvostele kaikki kategoriat")
    return redirect(f"/review/{id}#one")

@app.route("/restaurant/<int:id>", methods=["GET"])
def restaurant(id):
    #Information page
    data = db.select_restaurant(id)
    description = db.select_info_description(id)
    days = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    hours = db.select_info_hours(id)
    tags = db.select_tags(id)
    return render_template("demo_info.html", data=data, tags=tags, description=description, days=days, hours=hours, id=id)

@app.route("/admin")
def admin():
    #Admin register page
    try:
        if request.remote_addr == getenv("TRUSTED_IP"):
            return render_template("admin.html")
    except:
        flash("Jotain meni pahasti pieleen")
    flash("Non allowed IP address")
    return redirect("/")

#FUNCTIONALITY
#----------------
@app.route("/set_city", methods=["POST"])
def set_city():
    city = request.form["city"]
    set_session_city(city)
    return redirect("/#three")
      
# WARNING WEAK AUTHORIZATION HERE
@app.route("/delete_restaurant/<int:id>")
def delete_restaurant(id):
    if "user_id" in session:
        db.delete_restaurant(id)
        return redirect("/#one")
    flash("Istunto on vanhentunut")
    return redirect("/#one")

@app.route("/delete_review/<int:id>", methods=["POST"])
def delete_review(id):
    if "user_id" in session:
        review_id = request.form["review_id"]
        db.delete_review(review_id)
        return redirect("/demo_reviews/"+str(id))
    flash("Istunto on vanhentunut")
    return render_template("login_page.html")

@app.route("/update_info", methods=["POST"])
def update():
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
    #New restaurant
    name = request.form["name"]
    street = request.form["street"]
    city = request.form["city"]
    if city and street and name:
        restaurant_id = db.insert_restaurant(name, street, city)
        db.initiate_info(restaurant_id)
        return redirect("/#one")
    flash("Täytä nimi ja osoite tiedot")
    return redirect("/#one")

#AUTHENTICATION
#----------------
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
    session["city"] = "Helsinki"
    session["role"] = "user"
    return redirect("/#one")

@app.route("/register_admin", methods=["POST"])
def register_admin():
    return r.register_admin()

#Depricated
@app.route("/search/name")
def search_name():
    name = request.args["name"]
    restaurants = db.select_restaurants_name(name)
    return render_template("search_page.html", restaurants=restaurants)

#API
#----------------
@app.route("/api/restaurants", methods=["GET"])
def restaurants():
    response = utils.json_restaurants()
    return response

@app.route("/api/location", methods=["GET"])
def location():
    response = utils.json_location()
    return response

@app.route("/api/search/tags", methods=["POST"])
def seacrh_tags():
    body = request.get_json()
    print(body)
    return utils.json_search_result(body["tags"], body["mode"])