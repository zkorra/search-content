import requests

GOOGLE_API_KEY = "AIzaSyDy7a67ge1_rHrjm6JeGjeIrXMBix6Loow"
COUNT = 0


def fetch_search_api(searchEngineId, keyword, page, region):

    REGION_PARAM = ""

    if region:
        REGION_PARAM = f"&cr={region}"

    SEARCH_ENGINE_ID = searchEngineId

    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (int(page) - 1) * 10 + 1

    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={keyword}&start={start}{REGION_PARAM}"

    print(url)

    data = requests.get(url).json()

    return data
