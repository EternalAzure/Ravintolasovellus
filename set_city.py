import re
from flask import flash, session
import sys

def set_city(city):
  regex = "\\b[A-Z].*?\\b"
  format = re.compile(regex)  
  k = re.search(format, city)

  if k is None :
    flash("Vaaditaan iso alkukirjain")
    log("Didn't set session 'city' to "+city)
    return False
  else :
    session["city"] = city
    log("Did set session 'city' to "+city)
    log(f"Proof: {session['city']}")
    return True

def log(m):
    print("LOG: " + str(m), file=sys.stdout)