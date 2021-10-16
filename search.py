import db
import json, collections

def tag_or(tags):
    #loose search
    dictionary = {}
    for tag in tags:
        result_list = db.select_restaurants_tag(tag)
        for result in result_list:
            dictionary[result.id] = result
            
    restaurants = []
    for key in dictionary:
        restaurants.append(dictionary[key])
    print(restaurants)
    return restaurants

def tag_and(tags):
    #strict search
    results = {}
    restaurants = db.select_restaurants_all()
    #restaurant has to match all tags
    #breaks loop to save time
    for r in restaurants:
        matches_all = True
        for tag in tags:
            if not db.is_restaurant_tag(tag, r.id):
                matches_all = False
                break
        if matches_all:
            results[r.id] = r

    restaurants = []
    for key in results:
        restaurants.append(results[key])
    print(restaurants)
    return restaurants


def tags(tags, mode):
    results = None

    if mode == "AND":
        results = tag_and(tags)
    elif mode == "OR":
        results = tag_or(tags)
    else:
        return json.dumps([])

    if not results: return json.dumps([])

    objects_list = []
    for row in results:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["city"] = row[2]
        d["rating"] = str(db.grades_full_summary(row[0]))
        objects_list.append(d)
    
    j = json.dumps(objects_list)
    return j

def name(name):
    results = db.select_restaurants_name(name)
    print(results)
    
    objects_list = []
    for row in results:
        d = collections.OrderedDict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["city"] = row[2]
        d["rating"] = str(db.grades_full_summary(row[0]))
        objects_list.append(d)
    
    j = json.dumps(objects_list)
    return j