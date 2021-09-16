from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv, name

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT id, name, created_at FROM restaurants ORDER BY id DESC"
    result = db.session.execute(sql)
    restaurants = result.fetchall()
    return render_template("index.html", restaurants=restaurants)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    address = request.form["address"]
    sql = "INSERT INTO restaurants (name, address, created_at) VALUES (:name, :address, NOW()) RETURNING id"
    result = db.session.execute(sql, {"name":name, "address":address})
    restaurants_id = result.fetchone()[0]
    reviews = request.form.getlist("review")
    for review in reviews:
        if review != "":
            sql = "INSERT INTO reviews (restaurants_id, review) VALUES (:restaurants_id, :review)"
            db.session.execute(sql, {"restaurants_id":restaurants_id, "review":review})
    db.session.commit()
    return redirect("/")

@app.route("/restaurant/<int:id>")
def restaurant(id):
    sql = "SELECT name FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    sql = "SELECT id, review FROM reviews WHERE restaurants_id=:id"
    result = db.session.execute(sql, {"id":id})
    reviews = result.fetchall()
    return render_template("restaurant.html", id=id, name=name, reviews=reviews)

@app.route("/result/<int:id>")
def result(id):
    sql = "SELECT name FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]

    sql = "SELECT r.review, a.grade FROM reviews r LEFT JOIN answers a " \
          "ON r.id=a.reviews_id WHERE r.restaurants_id=:restaurants_id"
    result = db.session.execute(sql, {"restaurants_id":id})
    reviews = result.fetchall()
    return render_template("result.html", name=name, reviews=reviews)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/answer", methods=["POST"])
def answer():
    restaurants_id = request.form["id"]
    query = "SELECT id FROM reviews WHERE restaurants_id=:id"
    result = db.session.execute(query, {"id":restaurants_id})
    reviews = result.fetchall()

    for review in reviews:
        grade = request.form[str(review.id)]
        sql = "INSERT INTO answers (reviews_id, grade, sent_at) VALUES (:reviews_id, :grade, NOW())"
        db.session.execute(sql, {"reviews_id":review.id, "grade":grade})
        db.session.commit()
        
    return redirect("/result/" + str(restaurants_id))



