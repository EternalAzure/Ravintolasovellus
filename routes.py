from app import app
from flask_cors import CORS
from flask import render_template, request, redirect, session, flash
import utils, info, db
import auth, search
from set_city import set_city as set_session_city
from os import getenv

#Lets client request data from static/index.js through API
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# IMAGE
#----------------
@app.route("/show/<int:id>")
def show(id):
    image = db.select_image(id)
    if image:return image
    return "No image"


#WEB PAGES
#----------------
@app.route("/")
def index():
    url = getenv("MAP")
    list = utils.sorted_restaurants()
    return render_template("index.html", url=url, restaurants=list)

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
    if not utils.insert_grades(id):
        flash("Arvostele kaikki kategoriat")
    return redirect(f"/review/{id}#one")

@app.route("/info/<int:id>", methods=["GET"])
def restaurant(id):
    data = db.select_restaurant(id)
    description = db.select_info_description(id)
    days = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    hours = db.select_info_hours(id)
    tags = db.select_tags(id)
    return render_template("info.html", data=data, tags=tags, description=description, days=days, hours=hours, id=id)

@app.route("/admin")
def admin():
    #Admin register page
    try:
        if request.remote_addr == getenv("TRUSTED_IP"):
            return render_template("admin.html")
    except:
        flash("Joko html tiedoston nimi tai sijainti on väärä. \n "\
            "Tai serverin ympäristömuuttuja on nimetty väärin.")
    flash("Non allowed IP address")
    return redirect("/#one")


#FUNCTIONALITY
#----------------
# Update restaurant info
@app.route("/info/<int:id>/image", methods=["POST"])
def update_image(id):
    return info.image(request.files["file"], id)

@app.route("/info/<int:id>/tag", methods=["POST"])
def update_tag(id):
    return info.tag(request.form["tag"], id)

@app.route("/info/<int:id>/description", methods=["POST"])
def update_description(id):
    return info.description(request.form["description"], id)

@app.route("/info/<int:id>/hours", methods=["POST"])
def update_hours(id):
    days = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    hours = []
    for d in days:
        opening = request.form["opening_"+d]
        closing = request.form["closing_"+d]
        hours.append([opening, closing])
    return info.hours(hours, id)
#------

# Delete stuff
@app.route("/delete_restaurant/<int:id>")
def delete_restaurant(id):
    if "user_id" in session and session["role"] == "admin":
        db.delete_restaurant(id)
        return redirect("/#one")
    flash("Istunto on vanhentunut")
    return redirect("/#one")

@app.route("/delete_review/<int:id>", methods=["POST"])
def delete_review(id):
    if "user_id" in session:
        if session["user_id"] == id or session["role"] == "admin":
            review_id = request.form["review_id"]
            db.delete_review(review_id)
            return redirect("/review/"+str(id))

    flash("Istunto on vanhentunut")
    return redirect("/#one")
#------

@app.route("/set_city", methods=["POST"])
def set_city():
    city = request.form["city"]
    set_session_city(city)
    return redirect("/#three")
#------

# Create restaurant
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
    return auth.register_user()

@app.route("/login",methods=["POST"])
def login():
    return auth.login()

@app.route("/logout")
def logout():
    delete = [key for key in session]
    for key in delete: del session[key]
    session["city"] = "Helsinki"
    session["role"] = "user"
    return redirect("/#one")

@app.route("/register_admin", methods=["POST"])
def register_admin():
    return auth.register_admin()
#----------------

# Depricated
# Dont delete change to api format maybe
@app.route("/search/name")
def search_name_depricated():
    name = request.args["name"]
    list = db.select_restaurants_name(name)
    url = getenv("MAP")
    return render_template("index.html", url=url, restaurants=list)

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
def search_tags():
    body = request.get_json()
    return search.tags(body["tags"], body["mode"])

@app.route("/api/search/name", methods=["POST"])
def search_name():
    body = request.get_json()
    print(body)
    return search.name(body["name"])