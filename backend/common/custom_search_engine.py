import requests
from flask import request, make_response
from common.exceptions import exception_common, exception_cse
from common.dataframe_preparation.article import filter_article_property
from common.dataframe_preparation.course import filter_course_property
from config.secret import get_google_api_key


def handle_clean_data(data, content_type):
    if (content_type == "article"):
        filterArticle = filter_article_property(data)
        return filterArticle
    elif(content_type == "course"):
        filterCourse = filter_course_property(data)
        return filterCourse
    else:
        pass


def fetch(request):

    GOOGLE_API_KEY = get_google_api_key()

    content_type = request.args.get('type', '')
    search_engine_id = request.args.get('cx', '')
    keyword = request.args.get('query', '')
    page = request.args.get('page', '1')
    region = request.args.get('region', '')

    if not content_type:
        return exception_common('Content Type is missing', 400)
    elif content_type != 'article' and content_type != 'course':
        return exception_common('Content Type must be article or course, but we received ' + content_type, 400)

    if not search_engine_id:
        return exception_common('Search Engine ID is missing', 400)

    if not keyword:
        return exception_common('Keyword is missing', 400)

    REGION_PARAM = ""

    if region:
        REGION_PARAM = f"&cr={region}"

    SEARCH_ENGINE_ID = search_engine_id

    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (int(page) - 1) * 10 + 1

    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={keyword}&start={start}{REGION_PARAM}"

    response_data = requests.get(url).json()

    if response_data.get("error"):
        searchEngineError = response_data.get("error")
        return exception_cse(searchEngineError.get(
            "message"), searchEngineError.get("code"))

    if not response_data.get("items"):
        return exception_common(
            "No result found, try another keyword", 404)

    response_cleaned_data = handle_clean_data(response_data, content_type)

    return make_response(response_cleaned_data, 200)
