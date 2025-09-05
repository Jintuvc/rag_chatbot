# map.py
import requests
import os

GOOGLE_API_KEY = "AIzaSyAsSsYV9W427vkLCc9nPIeePESAmdKwF7E"
BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_places(query, location="India"):
    params = {
        "query": f"{query} {location}",
        "key": GOOGLE_API_KEY
    }
    resp = requests.get(BASE_URL, params=params)
    data = resp.json()
    if "results" in data and data["results"]:
        places = []
        for r in data["results"][:5]:
            places.append({
                "name": r.get("name"),
                "address": r.get("formatted_address"),
                "rating": r.get("rating", "N/A")
            })
        return places
    else:
        return {"Error": "No results found"}
