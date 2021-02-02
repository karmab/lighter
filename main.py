#!/usr/bin/python
# coding=utf-8

from flask import Flask, request, jsonify
import os
import re
import yaml


def decisionmaker(form):
    result = None
    for key1 in form:
        for key2 in settings:
            rule = settings[key2]
            if rule.get('match', 'fqdn') == key1 and re.match(rule['value'], form[key1]):
                print("Matching for %s" % key1)
                if 'mcp' in rule:
                    result = rule['mcp']
                    break
                else:
                    print("Missing mcp for %s" % key1)
    return result


app = Flask(__name__)
try:
    app.config.from_object('settings')
    config = app.config
except ImportError:
    config = {'PORT': os.environ.get('PORT', 9000)}

debug = config['DEBUG'] if 'DEBUG' in list(config) else False
port = int(config['PORT']) if 'PORT' in list(config) else 9000
config_dir = '/config' if 'KUBERNETES_PORT' in os.environ else '.'

with open("%s/settings.yml" % config_dir) as f:
    try:
        settings = yaml.safe_load(f)
    except Exception as e:
        print("Hit %s when reading settings.yml file" % e)
        os._exit(1)


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
