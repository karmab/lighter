#!/usr/bin/python
# coding=utf-8

from flask import Flask, request, jsonify
import os


def decisionmaker(form):
    print(form)
    return "proutos"


app = Flask(__name__)
try:
    app.config.from_object('settings')
    config = app.config
except ImportError:
    config = {'PORT': os.environ.get('PORT', 9000)}

debug = config['DEBUG'] if 'DEBUG' in list(config) else False
port = int(config['PORT']) if 'PORT'in list(config) else 9000


@app.route('/', methods=['POST'])
def index():
    """
    entry point
    """
    form = request.get_json()
    data = decisionmaker(form)
    if data is None:
        result = {'result': 'failure', 'reason': "Missing data"}
        response = jsonify(result)
        response.status_code = 400
    else:
        result = {'result': 'success', 'data': data}
        response = jsonify(result)
        response.status_code = 200
    return response


def run():
    """

    """
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    run()
