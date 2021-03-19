from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from custom_search_engine import fetchCustomSearch
from article import filterArticleProperty
import json
import traceback

app = Flask(__name__)
CORS(app)


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

    response = fetchCustomSearch(searchEngineId, keyword, page, region)

    if response.get("error"):
        searchEngineError = response.get("error")
        raise APICustomSearchEngineError(searchEngineError.get(
            "message"), searchEngineError.get("code"))
    
    if not response.get("items"):
        raise APINotFound("No result found, try another keyword")

    if(contentType == "article"):
        filterArticle = filterArticleProperty(response)
        return Response(response=filterArticle, status=200, mimetype='application/json')
    elif(contentType == "course"):
        pass


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
