from flask import Flask, request
from flask_cors import cross_origin
from common import custom_search_engine, engines_management, cse_management

app = Flask(__name__)


@app.route("/fetch_custom_search", methods=['GET'])
@cross_origin()
def fetch_custom_search(request):

    if request.method == 'GET':
        response = custom_search_engine.fetch(request)

    return response


@app.route("/history", methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def history(request):

    if request.method == 'GET':
        if request.args.get('check'):
            response = cse_management.check_history(request)
        elif request.args.get('file'):
            response = cse_management.load_content_file(request)
        else:
            response = cse_management.fetch_history(request)
    if request.method == 'POST':
        response = cse_management.save_selected_data(request)
    if request.method == 'DELETE':
        response = cse_management.delete_history(request)

    return response


@app.route("/engine", methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def engine(request):

    if request.method == 'GET':
        response = engines_management.fetch_engines()
    if request.method == 'POST':
        response = engines_management.create_engine(request)
    if request.method == 'PUT':
        response = engines_management.update_engine(request)
    if request.method == 'DELETE':
        response = engines_management.delete_engine(request)

    return response


if __name__ == '__main__':
    app.debug = True
    app.run()
