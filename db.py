import sys

def restaurants(db):
    sql = "SELECT id, name, created_at FROM restaurants"
    result = db.session.execute(sql)
    return result.fetchall()

def restaurant(db, id):
    sql = "SELECT name FROM restaurants WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def categories(db):
    sql = "SELECT id, category FROM review_categories"
    result = db.session.execute(sql)
    return result.fetchall()

def category(db, id):
    sql = "SELECT category FROM review_categories WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def grades(db):
    sql = "SELECT id, grades FROM grades"
    result = db.session.execute(sql)
    return result.fetchall()

def gradesByRestaurant(db, id):
    sql = "SELECT id, grade FROM grades WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def reviews(db, id):
    sql = "SELECT id, content, sent_at FROM reviews WHERE restaurant_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def reviewTogether(db, id):
    sql = "SELECT 1.0*SUM(grade)/NULLIF(COUNT(grade), 0) AS average FROM grades " \
          "WHERE grades.restaurant_id=:restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":id})
    
    try:
        value = result.fetchone()[0]
        return round(value,  1)
    except:
        return None

def reviewSeparate(db, restaurant, c):
    sql = "SELECT r.category, 1.0*SUM(grade)/NULLIF(COUNT(grade), 0) AS average FROM review_categories r LEFT JOIN grades " \
          "ON r.id=grades.category_id WHERE grades.restaurant_id=:restaurant AND r.id=:category GROUP BY r.category"
    result = db.session.execute(sql, {"restaurant":restaurant, "category":c})

    name = category(db, c)
    try:
        values = result.fetchall()[0]
        rounded = [values[0], round(values[1], 1)]
        return rounded
    except:
        return (name, None)

def insertRestaurant(db, name, address):
    sql = "INSERT INTO restaurants (name, address, created_at) VALUES (:name, :address, NOW()) RETURNING id"
    result = db.session.execute(sql, {"name":name, "address":address})
    db.session.commit()
    return result

def insertReview(db, review, restaurant):
    sql = "INSERT INTO reviews (content, restaurant_id, sent_at) VALUES (:review, :restaurant, NOW())"
    db.session.execute(sql, {"review":review, "restaurant":restaurant})
    db.session.commit()

def insertGrade(db, grade, restaurant, category):
    sql = "INSERT INTO grades (grade, restaurant_id, category_id) VALUES (:grade, :r_id, :c_id)"
    db.session.execute(sql, {"grade":grade, "r_id":restaurant, "c_id":category})
    db.session.commit()