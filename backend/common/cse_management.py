from flask import request, jsonify, make_response, json
from datetime import datetime, timezone
import pytz
from google.cloud import firestore, storage
from common.exceptions import exception_common

db = firestore.Client()
history_ref = db.collection('history')

client = storage.Client()
bucket = client.get_bucket('search-content-project.appspot.com')


def fetch_history(request):
    """
        read() : Fetches documents from Firestore collection as JSON
        engine : Return document that matches query ID
        all_engines : Return all documents
    """

    all_history = []

    for doc in history_ref.stream():
        history = doc.to_dict()
        history["id"] = doc.id
        all_history.append(history)

    all_history.sort(key=lambda x: x['timestamp'], reverse=True)

    return make_response(jsonify(all_history), 200)


def load_file(request):
    """
        read() : Fetches documents from Firestore collection as JSON
        engine : Return document that matches query ID
        all_engines : Return all documents
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
        delete() : Delete a document from Firestore collection
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
        delete() : Delete a document from Firestore collection
    """

    docs = history_ref.where(u'saveMethod', u'==', save_method).where(u'contentType', u'==', content_type).where(u'searchEngineId', u'==', search_engine_id).where(
        u'keyword', u'==', keyword).where(u'page', u'==', page).where(u'region', u'==', region).stream()

    all_history = []

    for doc in docs:
        history = doc.to_dict()

        history_ref.document(doc.id).delete()
        blob = bucket.get_blob(str(history["filename"]))

        blob.delete()

    # history_ref.document(history["id"]).delete()

    # blob = bucket.get_blob(str(history["filename"]))

    # blob.delete()

    return make_response(jsonify({"success": True}), 200)


def init_current_time():
    utc_dt = datetime.now(timezone.utc)
    ICT = pytz.timezone("Asia/Bangkok")

    current_time = utc_dt.astimezone(ICT)

    return current_time


def generate_filename(keyword, content_type):
    indochina_time = init_current_time().strftime("%Y%m%d-%H%M%S%f")

    filename = f"{keyword}-{content_type}-{indochina_time}"

    return filename


def save_to_storage(data, save_method: str, content_type: str,
                    search_engine_id: str, keyword: str,  page: str, region: str):
    """Background Cloud Function to be triggered by Cloud Storage.  
    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the file is sent as a request to 
    """

    if save_method != 'all' and save_method != 'selected':
        return exception_common('Save Method must be all or selected, but we received ' + save_method, 400)

    filename = generate_filename(keyword, content_type)
    current_time = init_current_time()

    filename_json = f'{filename}.json'
    # declare your file name
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
        u'keyword': keyword,
        u'page': page,
        u'region': region,
        u'filename': filename_json,
        u'saveMethod': save_method,
    }

    history_ref.document().set(data)

    # data = '{"text":"{}"}'.format(contents)
    # response = requests.post(
    #     'https://your-instance-server/endpoint-to-download-files', headers=headers, data=data)
    return 'UPLOAD'


def check_history(request):

    content_type = request.args.get('type', '')
    search_engine_id = request.args.get('cx', '')
    keyword = request.args.get('query', '')
    page = request.args.get('page', '1')
    region = request.args.get('region', '')
    isCheck = request.args.get('check', 'false')

    if isCheck == 'false':
        return exception_common('Checking params need be true', 400)

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

    if not request.json['contentType']:
        return exception_common('Content type is missing', 400)

    if not request.json['searchEngineId']:
        return exception_common('Search engine ID is missing', 400)

    if not request.json['keyword']:
        return exception_common('Keyword is missing', 400)

    if not request.json['page']:
        page = "1"

    if not request.json['region']:
        region = ""

    if not request.json['data']:
        return exception_common('Content data is missing', 400)

    content_type = request.json['contentType']
    search_engine_id = request.json['searchEngineId']
    keyword = request.json['keyword']
    page = request.json['page']
    region = request.json['region']
    data = request.json['data']

    if page == "":
        page = "1"

    data_json = json.dumps(data, sort_keys=False)

    delete_history_by_condition(save_method='selected', content_type=content_type,
                                search_engine_id=search_engine_id, keyword=keyword,  page=page, region=region)

    save_to_storage(data=data_json, save_method='selected', content_type=content_type,
                    search_engine_id=search_engine_id, keyword=keyword,  page=page, region=region)

    return make_response(jsonify({"success": True}), 200)
