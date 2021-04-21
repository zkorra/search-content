from flask import request, jsonify, make_response, json
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
