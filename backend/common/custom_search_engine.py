import requests
from flask import request, make_response, json, jsonify
from google.cloud import storage, firestore
from common.exceptions import exception_common, exception_cse
from common.cse_management import save_to_storage, check_history
from common.dataframe_preparation.article import filter_article_property
from common.dataframe_preparation.course import filter_course_property
from config.secret import get_google_api_key


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

    response_cleaned_data = handle_cleaning_method(
        response_data, content_type)

    save_to_storage(data=response_cleaned_data, save_method='all', content_type=content_type,
                    search_engine_id=search_engine_id, keyword=keyword,  page=page, region=region)

    return make_response(response_cleaned_data, 200)


def handle_cleaning_method(data, content_type):
    if (content_type == "article"):
        filterArticle = filter_article_property(data)
        return filterArticle
    elif(content_type == "course"):
        filterCourse = filter_course_property(data)
        return filterCourse
    else:
        pass


# def init_current_time():
#     utc_dt = datetime.now(timezone.utc)
#     ICT = pytz.timezone("Asia/Bangkok")

#     current_time = utc_dt.astimezone(ICT)

#     return current_time


# def generate_filename(keyword, content_type):
#     indochina_time = init_current_time().strftime("%Y%m%d-%H%M%S%f")

#     filename = f"{keyword}-{content_type}-{indochina_time}"

#     return filename


# def save_to_storage(json_data, keyword, content_type, page, region):
#     """Background Cloud Function to be triggered by Cloud Storage.
#     Args:
#         data (dict): The Cloud Functions event payload.
#         context (google.cloud.functions.Context): Metadata of triggering event.
#     Returns:
#         None; the file is sent as a request to
#     """

#     filename = generate_filename(keyword, content_type)
#     current_time = init_current_time()

#     db = firestore.Client()
#     history_ref = db.collection('history')

#     # Get the bucket that the file will be uploaded to.
#     client = storage.Client()
#     bucket = client.get_bucket('search-content-project.appspot.com')

#     filename_json = f'{filename}.json'
#     # declare your file name
#     blob = bucket.blob(filename_json)

#     # upload json data were we will set content_type as json
#     blob.upload_from_string(
#         data=json.dumps(json_data),
#         content_type='application/json'
#     )

#     data = {
#         u'timestamp': current_time,
#         u'keyword': keyword,
#         u'contentType': content_type,
#         u'page': page,
#         u'region': region,
#         u'filename': filename_json
#     }

#     history_ref.document().set(data)

#     # data = '{"text":"{}"}'.format(contents)
#     # response = requests.post(
#     #     'https://your-instance-server/endpoint-to-download-files', headers=headers, data=data)
#     return 'UPLOAD'
