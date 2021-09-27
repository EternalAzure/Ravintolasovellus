import re
from flask import flash, session

def set_city(city):
  regex = "\\b[A-Z].*?\\b"
  format = re.compile(regex)  
  k = re.search(format, city)

  if k is None :
    flash("Vaaditaan iso alkukirjain")
    return False
  else :
    session["city"] = city
    return True
