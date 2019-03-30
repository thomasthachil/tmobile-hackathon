import requests
import json

API_KEY= 'clrMY4OZTkQRzoiXajI_mMvcoXfd93XwUvFKkW6Ll7oCFratiTmhiUKKkwcycdzSfegzNSVqdlpY_8JmILwgMNn1PqMR-xGZrq7FoTj6ORtmerhpOfZsEqFypK-eXHYx'
headers = {'Authorization': 'Bearer %s' % API_KEY}

url = 'https://api.yelp.com/v3/businesses/search'
params = {'term':'bookstore','location':'New York City'}

req = requests.get(url, params=params, headers=headers)

parsed = json.loads(req.text)

businesses = parsed["businesses"]

for business in businesses:
    print("Name:", business["name"])
    print("Rating:", business["rating"])
    print("Address:", " ".join(business["location"]["display_address"]))
    print("Phone:", business["phone"])
    print("\n")

    id = business["id"]

    url="https://api.yelp.com/v3/businesses/" + id + "/reviews"

    req = requests.get(url, headers=headers)

    parsed = json.loads(req.text)

    reviews = parsed["reviews"]

    print("--- Reviews ---")

    for review in reviews:
        print("User:", review["user"]["name"], "Rating:", review["rating"], "Review:", review["text"], "\n")
