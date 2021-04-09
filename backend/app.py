from flask import Flask, request, jsonify, Response, send_file
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
from custom_search_engine import fetch_search_api
from article import filter_article_property
from course import filter_course_property
import traceback

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('config/key.json')
default_app = initialize_app(cred)
db = firestore.client()
engine_ref = db.collection('engines')


class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APICustomSearchEngineError(APIError):
    description = "Custom Search Engine Error"


class APIBadRequest(APIError):
    code = 400
    description = "Bad Request"


class APINotFound(APIError):
    code = 404
    description = "Not found"


@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]

    if len(err.args) > 1:
        err.code = err.args[1]

    # Add some logging so that we can monitor different types of errors
    app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code


@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for any other server error"""
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(''.join(traceback.format_exception(
        etype=type(err), value=err, tb=err.__traceback__)))
    response = {
        "error": "Sorry, that error is on us, please contact support if this wasn't an accident"}
    return jsonify(response), 500


@app.route('/fetch', methods=['GET'])
def index():

    contentType = request.args.get('type', '')
    searchEngineId = request.args.get('cx', '')
    keyword = request.args.get('query', '')
    page = request.args.get('page', '1')
    region = request.args.get('region', '')

    if not contentType:
        raise APIBadRequest('Content Type is missing')
    elif contentType != 'article' and contentType != 'course':
        raise APIBadRequest(
            'Content Type must be article or course, but we received ' + contentType)

    if not searchEngineId:
        raise APIBadRequest('Search Engine ID is missing')

    if not keyword:
        raise APIBadRequest('Keyword is missing')

    response = fetch_search_api(searchEngineId, keyword, page, region)

    if response.get("error"):
        searchEngineError = response.get("error")
        raise APICustomSearchEngineError(searchEngineError.get(
            "message"), searchEngineError.get("code"))

    if not response.get("items"):
        raise APINotFound("No result found, try another keyword")

    if(contentType == "article"):
        filterArticle = filter_article_property(response)
        return Response(response=filterArticle, status=200, mimetype='application/json')
    elif(contentType == "course"):
        filterCourse = filter_course_property(response)
        return Response(response=filterCourse, status=200, mimetype='application/json')


@app.route('/engine', methods=['GET'])
def fetch_engine_list():
    return send_file('data/engine_list.json', cache_timeout=0), 200


@app.route('/engine/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        engine : Return document that matches query ID
        all_engines : Return all documents
    """
    try:
        all_engines = []

        for doc in engine_ref.stream():
            engine = doc.to_dict()
            engine["id"] = doc.id
            all_engines.append(engine)

        return jsonify(all_engines), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/engine/create', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'searchEngineId': '1f22',
            'name': 'myengine', 'contentType': 'article'}
    """
    try:
        engine_ref.document().set(request.json)
        search_engine_id = request.json['searchEngineId']
        docs = engine_ref.where(
            u'searchEngineId', u'==', search_engine_id).stream()
        for doc in docs:
            engine = doc.to_dict()
            engine["id"] = doc.id
        return jsonify(engine), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/engine/update', methods=['PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.args.get('id')
        engine_ref.document(id).update(request.json)
        doc = engine_ref.document(id).get()
        engine = doc.to_dict()
        engine["id"] = doc.id
        return jsonify(engine), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# @app.route('/delete', methods=['GET', 'DELETE'])
# def delete():
#     """
#         delete() : Delete a document from Firestore collection
#     """
#     try:
#         # Check for ID in URL query
#         todo_id = request.args.get('id')
#         todo_ref.document(todo_id).delete()
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
