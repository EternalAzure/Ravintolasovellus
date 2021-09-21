from flask import render_template, request, session, redirect
from db import insert_user, is_username_taken
import sys

def log(m):
    print("LOG: " + str(m), file=sys.stdout)


def register():
  username = request.form["username"]
  password = request.form["password"]
  
  a = validate_username_format(username)
  b = validate_password(password)
  message = "Nimen pitää olla enintään 15 merkkiä ja \n" \
            "salasanan välillä 5 - 50 merkkiä"
  if a and b:
    log("SYÖTE KUNNOSSA")
    if is_username_taken(username):
      message = "Username is taken"
      log("USERNAME TAKEN")
      return render_template("register_page.html.j2", message=message)
    else:
      log("USER REGISTERED")
      insert_user(username, password)
      session["username"] = username
      return render_template("register_page.html.j2")

  log("SYÖTE EI KUNNOSSA")
  return render_template("register_page.html.j2", message=message)

  
def validate_username_format(username):
    if not username: return False
    if len(username) > 15: return False
    return True

def validate_password(password):
    if not password: return False
    if len(password) < 5 or len(password) > 50 : return False
    return True
