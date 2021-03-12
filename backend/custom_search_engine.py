import requests

GOOGLE_API_KEY = "AIzaSyB6trExhF-mxOKdNQsAW-HkVOHBGV8W0R4"
COUNT = 0


def fetchCustomSearch(cx, query, page, region):

    REGION_PARAM = ""

    if region:
        REGION_PARAM = f"&cr={region}"

    SEARCH_ENGINE_ID = cx

    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (int(page) - 1) * 10 + 1

    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}{REGION_PARAM}"

    data = requests.get(url).json()

    return data