"""Main Entrypoint for the Application"""

import logging
import json

from flask import Flask, request
from flask import jsonify

import notebook


app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'


@app.route('/notes', methods=['POST', 'GET'])
def access_notes():
    """inserts and retrieves notes from datastore"""

    book = notebook.NoteBook()
    if request.method == 'GET':
        results = book.fetch_notes()
        result = [notebook.parse_note_time(obj) for obj in results]
        return jsonify(result)
    elif request.method == 'POST':
        print json.dumps(request.get_json())
        text = request.get_json()['text']
        book.store_note(text)
        return "done"


@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
