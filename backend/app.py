from flask import Flask, request
from custom_search_engine import fetchCustomSearch
from article import getArticles
app = Flask(__name__)


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return "Oops! Something went wrong.", 500


@app.route('/fetch', methods=['GET'])
def index():

    cx = request.args.get('cx', '')
    query = request.args.get('query', '')
    page = request.args.get('page', '1')
    region = request.args.get('region', '')

    response = fetchCustomSearch(cx, query, page, region)

    return getArticles(response)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
