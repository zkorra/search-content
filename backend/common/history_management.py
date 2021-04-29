from flask import request, jsonify, make_response, json
from datetime import datetime, timezone
import pytz
import urllib.parse
from google.cloud import firestore, storage
from common.exceptions import exception_common
from config.secret import get_storage_name

STORAGE_NAME = get_storage_name()

db = firestore.Client()
history_ref = db.collection('history')

client = storage.Client()
bucket = client.get_bucket(STORAGE_NAME)


def fetch_history(request):
    """
        fetch_history() : Fetches documents from Firestore collection as JSON
        all_history : Return all documents
    """

    all_history = []

    for doc in history_ref.stream():
        history = doc.to_dict()
        history["id"] = doc.id
        all_history.append(history)

    all_history.sort(key=lambda x: x['timestamp'], reverse=True)

    return make_response(jsonify(all_history), 200)


def load_content_file(request):
    """
        load_content_file() : Fetches json file from Cloud Storage
        file_data : Return file that matches param
    """

    filename = request.args.get('file')

    if not filename:
        return exception_common('Filename is missing', 400)

    if filename[-5:] != '.json':
        return exception_common('File format is missing', 400)

    blob = bucket.get_blob(filename)

    if not blob:
        return exception_common('No file found, try again', 404)

    file_data = json.loads(blob.download_as_string())

    return make_response(file_data, 200)


def delete_history(request):
    """
        delete_history() : Delete a document from Firestore collection and file from Cloud Storage
    """
    id = request.args.get('id')

    if not id:
        return exception_common('ID is missing', 400)

    doc = history_ref.document(id).get()
    history = doc.to_dict()

    history_ref.document(id).delete()

    blob = bucket.get_blob(str(history["filename"]))

    blob.delete()

    return make_response(jsonify({"success": True}), 200)


def delete_history_by_condition(save_method, content_type, search_engine_id, keyword, page, region):
    """
        delete_history_by_condition() : Delete a document from Firestore collection and file from Cloud Storage
    """

    keyword = urllib.parse.unquote(keyword)

    docs = history_ref.where(u'saveMethod', u'==', save_method).where(u'contentType', u'==', content_type).where(u'searchEngineId', u'==', search_engine_id).where(
        u'keyword', u'==', keyword).where(u'page', u'==', page).where(u'region', u'==', region).stream()

    all_history = []

    for doc in docs:
        history = doc.to_dict()

        history_ref.document(doc.id).delete()
        blob = bucket.get_blob(str(history["filename"]))

        blob.delete()

    return make_response(jsonify({"success": True}), 200)


def init_current_time():
    """
        init_current_time() : Init current Indochina time
    """
    utc_dt = datetime.now(timezone.utc)
    ICT = pytz.timezone("Asia/Bangkok")

    current_time = utc_dt.astimezone(ICT)

    return current_time


def generate_filename(keyword, content_type):
    """
        generate_filename() : Generate filename by keyword, content type and time
    """
    indochina_time = init_current_time().strftime("%Y%m%d-%H%M%S%f")

    filename = f"{keyword}-{content_type}-{indochina_time}"

    return filename


def save_to_storage(data, save_method: str, content_type: str,
                    search_engine_id: str, keyword: str,  page: str, region: str):

    if save_method != 'all' and save_method != 'selected':
        return exception_common('Save Method must be all or selected, but we received ' + save_method, 400)

    filename = generate_filename(keyword, content_type)
    current_time = init_current_time()

    filename_json = f'{filename}.json'

    blob = bucket.blob(filename_json)

    # upload json data were we will set content_type as json
    blob.upload_from_string(
        data=json.dumps(data),
        content_type='application/json'
    )

    data = {
        u'timestamp': current_time,
        u'contentType': content_type,
        u'searchEngineId': search_engine_id,
        u'keyword': urllib.parse.unquote(keyword),
        u'page': page,
        u'region': region,
        u'filename': filename_json,
        u'saveMethod': save_method,
    }

    history_ref.document().set(data)

    return 'UPLOADED'


def check_history(request):

    content_type = request.args.get('type', '')
    search_engine_id = request.args.get('cx', '')
    keyword = request.args.get('query', '')
    page = request.args.get('page', '1')
    region = request.args.get('region', '')
    isCheck = request.args.get('check', 'false')

    if not content_type:
        return exception_common('Content Type is missing', 400)
    elif content_type != 'article' and content_type != 'course':
        return exception_common('Content Type must be article or course, but we received ' + content_type, 400)

    if not search_engine_id:
        return exception_common('Search Engine ID is missing', 400)

    if not keyword:
        return exception_common('Keyword is missing', 400)

    if isCheck != 'true':
        return exception_common('Checking params need be true', 400)

    keyword = urllib.parse.unquote(keyword)

    docs = history_ref.where(u'contentType', u'==', content_type).where(u'searchEngineId', u'==', search_engine_id).where(
        u'keyword', u'==', keyword).where(u'page', u'==', page).where(u'region', u'==', region).stream()

    all_history = []
    recent_history = []

    for doc in docs:
        history = doc.to_dict()
        history["id"] = doc.id
        all_history.append(history)

    if all_history:
        all_history.sort(key=lambda x: x['timestamp'], reverse=True)
        recent_history = [all_history[0]]

    return make_response(jsonify(recent_history), 200)


def save_selected_data(request):

    content_type = request.json['contentType']
    search_engine_id = request.json['searchEngineId']
    keyword = request.json['keyword']
    page = request.json['page']
    region = request.json['region']
    data = request.json['data']

    if not content_type:
        return exception_common('Content type is missing', 400)

    if not search_engine_id:
        return exception_common('Search engine ID is missing', 400)

    if not keyword:
        return exception_common('Keyword is missing', 400)

    if not page:
        page = "1"

    if not region:
        region = ""

    if not data:
        return exception_common('Content data is missing', 400)

    data_json = json.dumps(data, sort_keys=False)

    delete_history_by_condition(save_method='selected', content_type=content_type,
                                search_engine_id=search_engine_id, keyword=keyword,  page=page, region=region)

    save_to_storage(data=data_json, save_method='selected', content_type=content_type,
                    search_engine_id=search_engine_id, keyword=keyword,  page=page, region=region)

    return make_response(jsonify({"success": True}), 200)
