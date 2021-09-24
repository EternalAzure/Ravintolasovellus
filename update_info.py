from flask import render_template
import db
import sys
import re
import time

# For user to read in update_response.html.j2
errors = []

def handle_input(hours, description, tag, id):
  input = {}

  #1. Validate input
  if validate_id(id):
    input["id"] = int(id)
  else:
    return render_template("update_response.html.j2", errors=errors, id=id)
  
  if validate_description(description):
    input["description"] = description
  
  if validate_tag(tag):
    input["tag"] = tag
  
  input["hours"] = validate_hours(hours, id)

  #2. Use data
  update(input)

  #3. User feedback
  return render_template("update_response.html.j2", correct_input=input, id=id)

#Check if such restaurant exists
def validate_id(id):
  restaurant = db.select_restaurant(id)
  if not restaurant:
    errors.append("Ravintolaa, jonka tietoja päivitit ei löytynyt")
    return False

  if not db.is_info_ref(id):
    print("row in table info for "+id+" was not initiated", file=sys.stderr)
    db.initiate_info(id)
    
  return True

def validate_hours(hours, id):
  valid = db.select_info_hours(id)

  for i in range(7):
    opening = hours[i][0]
    closing = hours[i][1]
    try:
      #Check if 24h format
      opening_time = time.strptime(opening, '%H:%M')
      closing_time = time.strptime(closing, '%H:%M')
      #Check times are logical
      if opening_time < closing_time:
        valid[i][0] = opening
        valid[i][1] = closing
    except ValueError: # default to previous
      pass

  return valid


# No more than 1500 characters
def validate_description(input):
  if not input:
    return False

  value = str(input)
  if len(value) > 1500:
    errors.append("Ravintolan kuvaus on liian pitkä. Käytä enintään 1500 merkkiä")
    return False

  return True

# One word
def validate_tag(input):
  text = str(input)
  words = text.split()
  # empty input should not give error mesage to user
  if not input:
    return False

  if len(text) > 20 or len(words) > 1:
    errors.append("Tunnisteeksi kelpaa yksi sana, jonka pituus on max 20 merkkiä")
    return False
  return True

def update(input):
  log("UPDATE")
  log(input["hours"])
  try:
    db.update_info_hours(input["hours"], input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  try:
    db.update_info_description(input["description"], input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  tags = []
  try:
    tags = db.select_info_tags(input["id"])
    tags.append(input["tag"])
    db.update_info_tags(tags, input["id"])
  except TypeError:
    pass
  except KeyError:
    pass
  log("/UPDATE")
  


def log(m):
    print("LOG: " + str(m), file=sys.stdout)