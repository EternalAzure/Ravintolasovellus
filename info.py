from flask import flash
from werkzeug.utils import redirect
import db
import time, re

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
    if not name.endswith(".jpg"):
        flash('Kelvoton tiedostonimi. Käytä .jpg.')
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

def hours(hours, id):
    if not validate_id(id):
        return redirect(f"/info/{id}#three")

    hours = validate_hours(hours, id)
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
    url = re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?[.](?:com|io|fi|de|fr|uk|ee|es|pl|ru)', homepage)
    print(url)
    if url:
        db.update_info_homepage(homepage, id)
        return redirect(f"/info/{id}#one")
    flash("Kelvoton url")
    return redirect(f"/info/{id}#three")