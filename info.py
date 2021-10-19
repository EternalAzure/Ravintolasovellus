from flask import flash
from werkzeug.utils import redirect
import db
import time, re

def restaurant(name, street, city):
    x = re.search(r"\D{1,30}\s[0-9]{1,}$", street)

    if x == None or x.group() != street:
        flash("Kadun nimen pitää olla enintään \n30 merkkiä ja loppua numeroon")
        return redirect("/#one")

    restaurant_id = db.insert_restaurant(name, street, city)
    db.initiate_info(restaurant_id)
    return redirect(f"/info/{restaurant_id}")

#Check if such restaurant exists
def validate_id(id):
    restaurant = db.select_restaurant(id)
    if not restaurant:
        flash("Ravintolaa, jonka tietoja päivitit ei löytynyt")
        return False

    if not db.is_info_ref(id):
        db.initiate_info(id)
      
    return True

def image(file, id):
    if not validate_id(id):
        return redirect(f"/info/{id}#three")

    name = file.filename
    error = False
    if not name.endswith(".jpg") and not name.endswith(".jpeg"):
        flash('Kelvoton tiedostonimi. Käytä .jpg tai .jpeg')
        error = True

    data = file.read()

    if len(data) > 200*1024:
        flash('Tiedosto saa olla enintään 204kt. ')
        error = True

    if error:
        return redirect(f"/info/{id}#three")

    image = db.select_image(id)
    if image:
        db.update_image(data, id)
        return redirect(f"/info/{id}#one")

    db.insert_image(name, data, id)
    return redirect(f"/info/{id}#one")

def tag(tag, id):
    if not validate_id(id):
        return redirect(f"/info/{id}#three")

    # empty input should not give error message to user
    if not tag:
        return redirect(f"/info/{id}#one")

    if validate_tag(tag):
        db.update_tags(tag, id)
        return redirect(f"/info/{id}#one")
    return redirect(f"/info/{id}#three")

def validate_tag(input):
    text = str(input)
    words = text.split()

    if len(text) > 20 or len(words) > 1:
        flash("Tunnisteeksi kelpaa yksi sana, \njonka pituus on max 20 merkkiä")
        return False
    return True

def description(input, id):
    if not validate_id(id):
        return redirect(f"/info/{id}#three")

    if validate_description(input):
        db.update_info_description(input, id)
        return redirect(f"/info/{id}#one")
    return redirect(f"/info/{id}#three")

def validate_description(input):
  # Limit to about 130 in finnish
    if not input:
        return False

    value = str(input)
    if len(value) > 875:
        flash("Käytä enintään 875 merkkiä eli noin 130 sanaa\n")
        return False
    return True

def hours(hours, closed_or_not, id):
    print("hours()")
    print(closed_or_not)
    print(hours)
    if not validate_id(id):
        return redirect(f"/info/{id}#three")

    hours = validate_hours(hours, id)
    print(hours)
    index = 0
    for status in closed_or_not:
        print("index", index)
        if status == "on":
            hours[index][0] = "suljettu"
            hours[index][1] = "suljettu"
        index += 1

    db.update_info_hours(hours, id)
    return redirect(f"/info/{id}#one")

def validate_hours(hours, id):
    valid = db.select_info_hours(id)

    for i in range(7):
        opening = hours[i][0]
        closing = hours[i][1]
        try:
            #Check if 24h format
            time.strptime(opening, '%H:%M')
            time.strptime(closing, '%H:%M')

            valid[i][0] = opening
            valid[i][1] = closing
        except ValueError: # default to previous
            pass
    return valid

def homepage(homepage, id):
    # Wont stop admins from giving more than one urls as one, but we trust them not to
    url = re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?[.](?:com|io|fi|de|fr|uk|ee|es|pl|ru)', homepage)
    print(url)
    if url:
        db.update_info_homepage(homepage, id)
        return redirect(f"/info/{id}#one")
    flash("Kelvoton url")
    return redirect(f"/info/{id}#three")