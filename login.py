from werkzeug.utils import redirect
from db import verify_user, select_users_id, select_users_role, select_users_city
from flask import request, redirect, session, flash

def login():
  username = request.form["username"]
  password = request.form["password"]
  if verify_user(username, password):
      session["username"] = username
      session["user_id"] = select_users_id(username)
      session["role"] = select_users_role(username)
      session["city"] = select_users_city(username)
      return redirect("/#one")
  flash("Väärä käyttäjänimi tai salasana")
  return redirect("/#one")