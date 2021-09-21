from db import verify_user
from flask import request, render_template, session

def login():
  username = request.form["username"]
  password = request.form["password"]
  if verify_user(username, password):
      session["username"] = username
  return render_template("/login_page.html.j2", message="Väärä käyttäjänimi tai salasana")