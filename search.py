from flask import session
import sys
from db import select_restaurants_tag, select_restaurants_limited, is_restaurant_tag

def tag_or(key):
    #inclusive search
    #very inefficient
    log("tag_OR")
    search_tags = session["search_tags"]
    search_tags[key] = key
    session["search_tags"] = search_tags
    no_duplicates = {}
    for key in search_tags:
        result_list = select_restaurants_tag(search_tags[key])
        for result in result_list:
            no_duplicates[result.id] = result
            
    restaurants = []
    for key in no_duplicates:
        restaurants.append(no_duplicates[key])
    return restaurants

def tag_and(key):
    #exclusive search
    #Some what inefficient
    log("tag_AND")
    city = "Helsinki"
    if "city" in session:
        city = session["city"]
    
    search_tags = session["search_tags"]
    search_tags[key] = key
    session["search_tags"] = search_tags

    results = {}
    restaurants = select_restaurants_limited(city)
    #restaurant has to match all tags
    #breaks loop to save time
    for r in restaurants:
        matches_all = True
        for tag in search_tags:
            if not is_restaurant_tag(tag, r.id):
                matches_all = False
                break
        if matches_all:
            results[r.id] = r

    restaurants = []
    for key in results:
        restaurants.append(results[key])
    return restaurants

def log(m):
    print("LOG: " + str(m), file=sys.stdout)