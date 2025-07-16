# scraper.py

import requests

def get_sample_data(limit=5):
    print("Querying Product Hunt API...")

    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {
        "Authorization": "Bearer Z2-e4F0oQuaRjlbwEMnNhdeBc0-wucXKuhjwYRo31uU",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    query = f"""
    {{
      posts(order: VOTES, first: {limit}) {{
        edges {{
          node {{
            name
            tagline
            votesCount
            commentsCount
            topics {{
              edges {{
                node {{
                  name
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(url, json={'query': query}, headers=headers)

    if response.status_code != 200:
        print("Error fetching data:", response.text)
        return []

    try:
        json_data = response.json()
        products = []
        for edge in json_data["data"]["posts"]["edges"]:
            node = edge["node"]
            product = {
                "name": node["name"],
                "tagline": node["tagline"],
                "upvotes": node["votesCount"],
                "comments": node["commentsCount"],
                "tags": [t["node"]["name"] for t in node["topics"]["edges"]]
            }
            products.append(product)

        print("Retrieved", len(products), "products")
        return products

    except Exception as e:
        print("Failed to parse response:", e)
        return []
