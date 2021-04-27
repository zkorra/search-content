from flask import request, jsonify, make_response
from google.cloud import firestore
from common.exceptions import exception_common, exception_firestore

db = firestore.Client()
engine_ref = db.collection('engines')


def fetch_engines():
    """
        fetch_engines() : Fetches documents from Firestore collection as JSON
        all_engines : Return all documents
    """
    all_engines = []

    for doc in engine_ref.stream():
        engine = doc.to_dict()
        engine["id"] = doc.id
        all_engines.append(engine)

    return make_response(jsonify(all_engines), 200)


def create_engine(request):
    """
        create_engine() : Add document to Firestore collection with request body
        Ensure you pass a Search Engine ID as part of json body in post request
        e.g. json={'searchEngineId': '1f22ff85',
            'name': 'myengine', 'contentType': 'article'}
    """

    if not request.json['searchEngineId']:
        return exception_common('Search engine ID is missing', 400)

    if not request.json['name']:
        return exception_common('Engine name is missing', 400)

    if not request.json['contentType']:
        return exception_common('Content type is missing', 400)

    engine_ref.document().set(request.json)
    search_engine_id = request.json['searchEngineId']

    # Get created engine in firestore
    docs = engine_ref.where(
        u'searchEngineId', u'==', search_engine_id).stream()
    for doc in docs:
        engine = doc.to_dict()
        engine["id"] = doc.id

    return make_response(jsonify(engine), 200)


def update_engine(request):
    """
        update_engine() : Update document in Firestore collection with request body
        Ensure you pass a Search Engine ID as part of json body in post request
        e.g. json={'searchEngineId': '1f22',
            'name': 'myengine', 'contentType': 'article'}
    """
    id = request.args.get('id')

    if not id:
        return exception_common('ID is missing', 400)

    if not request.json['searchEngineId']:
        return exception_common('Search engine ID is missing', 400)

    if not request.json['name']:
        return exception_common('Engine name is missing', 400)

    if not request.json['contentType']:
        return exception_common('Content type is missing', 400)

    engine_ref.document(id).update(request.json)

    # Get created engine in firestore
    doc = engine_ref.document(id).get()
    engine = doc.to_dict()
    engine["id"] = doc.id

    return make_response(jsonify(engine), 200)


def delete_engine(request):
    """
        delete_engine() : Delete a document from Firestore collection
    """
    id = request.args.get('id')

    if not id:
        return exception_common('ID is missing', 400)

    engine_ref.document(id).delete()

    return make_response(jsonify({"success": True}), 200)
