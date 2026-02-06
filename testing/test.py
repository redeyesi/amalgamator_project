params = {
    "q": "debate",
    "api-key": API_KEY,
    "format": "json",
    "order-by": "newest",
    "query-fields": "headline,body",
    "show-fields": "headline,byline,publication",
    "shouldHideAdverts": "true",
    "page-size": 100,
}

response = requests.get(url, params=params)
data = response.json()

# Extract unique sectionIds
section_ids = set()
for article in data.get("response", {}).get("results", []):
    section_id = article.get("sectionId")
    if section_id:
        section_ids.add(section_id)

print("Unique sectionIds:", section_ids)
