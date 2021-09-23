from db import verify_user, select_users_id, select_users_role
from flask import request, render_template, session

def login():
  username = request.form["username"]
  password = request.form["password"]
  if verify_user(username, password):
      session["username"] = username
      session["user_id"] = select_users_id(username)
      session["role"] = select_users_role(username)
  return render_template("/login_page.html.j2", message="Väärä käyttäjänimi tai salasana")