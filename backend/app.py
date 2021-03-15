from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from custom_search_engine import fetchCustomSearch
from article import filterArticleProperty

app = Flask(__name__)
CORS(app)


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return "Oops! Something went wrong.", 500


@app.route('/fetch', methods=['GET'])
def index():

    category = request.args.get('type', '')
    cx = request.args.get('cx', '')
    query = request.args.get('query', '')
    page = request.args.get('page', '1')
    region = request.args.get('region', '')

    response = fetchCustomSearch(cx, query, page, region)

    if(category == 'article'):
        filterArticle = filterArticleProperty(response)
        return Response(response=filterArticle, status=200, mimetype='application/json')
    else:
        return 0


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
