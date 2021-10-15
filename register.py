from flask import render_template, request, session, redirect, flash
from db import insert_user, is_username_taken, select_users_id
import utils

def register_user():
  username = request.form["username"]
  password = request.form["password"]
  city = request.form["city"]

  if not utils.firts_letter_capital(city):
    flash("Iso alkukirjain kaupungin nimeen")
    return redirect("/#one")

  a = validate_username_format(username)
  b = validate_password(password)

  if a and b:
    if is_username_taken(username):
      flash("Käyttäjänimi on varattu")
      return redirect("/#one")
    else:
      insert_user(username, password, "user", city)
      session["username"] = username
      session["role"] = "user"
      session["user_id"] = select_users_id(username)
      session["city"] = city
      return redirect("/#one")

  flash("Nimen pitää olla enintään 15 merkkiä ja \n" \
        "salasanan välillä 5 - 50 merkkiä")
  return redirect("/#one")

def register_admin():
  username = request.form["username"]
  password = request.form["password"]
  a = validate_username_format(username)
  b = validate_password(password)
  message = "Nimen pitää olla enintään 15 merkkiä ja \n" \
            "salasanan välillä 5 - 50 merkkiä"
  if a and b:
    if is_username_taken(username):
      message = "Username is taken"
      return render_template("admin.html", message=message)
    else:
      insert_user(username, password, "admin", "Helsinki")
      session["username"] = username
      session["role"] = "admin"
      session["user_id"] = select_users_id(username)
      return render_template("admin.html")

  return render_template("admin.html", message=message)

  
def validate_username_format(username):
    if not username: return False
    if len(username) > 15: return False
    return True

def validate_password(password):
    if not password: return False
    if len(password) <= 5 or len(password) <= 50 : return False
    return True
