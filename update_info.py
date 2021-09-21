from flask import render_template
import db
import sys

def handle_input(opening, closing, description, tag, id):
  
  input = {}
  log("INPUT")
  log(opening)
  log(closing)
  log(description)
  log(tag)
  log(id)
  log("/INPUT")

  #1. Validate input
  if validate_id(id):
    input["id"] = int(id)
    log("id is valid")
  else:
    return render_template("update_response.html.j2", correct_input=input, id=id)
  if validate_opening(opening):
    input["opening"] = opening
    log("opening is valid")
  if validate_closing(closing):
    input["closing"] = closing
    log("closing is valid")
  if validate_description(description):
    input["description"] = description
    log("description is valid")
  if validate_tag(tag):
    input["tag"] = tag
    log("tag is valid")

  #2. Use data
  update(input)

  #3. User feedback
  return render_template("update_response.html.j2", correct_input=input, id=id)

def validate_id(id):
  #Check such restaurant exists
  #
  return True

def validate_opening(input):
  #
  #
  if input == '' or None:
    return False
  return True

def validate_closing(input):
  #
  #
  if input == '' or None:
    return False
  return True

def validate_description(input):
  #
  #
  if input == '' or None:
    return False
  return True

def validate_tag(input):
  #
  #
  if input == '' or None:
    return False
  return True

def update(input):
  log("UPDATE")
  try:
    db.update_info_opening(input["opening"], input["id"])
  except TypeError:
    log("opening TypeError")
    pass
  except KeyError:
    log("opening KeyError")
    pass
  try:
    db.update_info_closing(input["closing"], input["id"])
  except TypeError:
    log("closing TypeError")
    pass
  except KeyError:
    log("closing KeyError")
    pass
  try:
    db.update_info_description(input["description"], input["id"])
  except TypeError:
    log("description TypeError")
    pass
  except KeyError:
    log("description KeyError")
    pass
  tags = []
  try:
    tags = db.select_info_tags(input["id"])
    tags.append(input["tag"])
    db.update_info_tags(tags, input["id"])
  except TypeError:
    log("tag TypeError")
    pass
  except KeyError:
    log("tag KeyError")
    pass
  log("/UPDATE")
  

def log(m):
    print("LOG: " + str(m), file=sys.stdout)