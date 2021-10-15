from flask import session
from db import select_restaurants_tag, select_restaurants_limited, is_restaurant_tag
import json, collections

def tag_or(tags):
    #inclusive search
    dictionary = {}
    for tag in tags:
        result_list = select_restaurants_tag(tag)
        for result in result_list:
            dictionary[result.id] = result
            
    restaurants = []
    for key in dictionary:
        print(key)
        restaurants.append(dictionary[key])
    return restaurants

def tag_and(tags):
    #exclusive search
    #Some what inefficient
    city = "Helsinki"
    if "city" in session:
        city = session["city"]
    
    results = {}
    restaurants = select_restaurants_limited(city)
    #restaurant has to match all tags
    #breaks loop to save time
    for r in restaurants:
        matches_all = True
        for tag in tags:
            if not is_restaurant_tag(tag, r.id):
                matches_all = False
                break
        if matches_all:
            results[r.id] = r

    restaurants = []
    for key in results:
        restaurants.append(results[key])
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
        objects_list.append(d)
    
    j = json.dumps(objects_list)
    return j