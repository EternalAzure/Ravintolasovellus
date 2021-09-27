from flask import session
import sys
from db import select_restaurants_name, select_restaurants_tag

def tag_and(tag):
    log("tag_AND")
    search_tags = session["search_tags"]
    search_tags.append(tag)
    session["search_tags"] = search_tags
    restaurants = []
    log(search_tags)
    for tag in search_tags:
        log("tag:"+tag)
        result_list = select_restaurants_tag(tag)
        log(result_list)
        for result in result_list:
            log(result)
            restaurants.append(result)
    log(restaurants)
    log("/tag_and")
    return restaurants

def log(m):
    print("LOG: " + str(m), file=sys.stdout)