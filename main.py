#!/usr/bin/python
# coding=utf-8

from flask import Flask, request, jsonify
from kubernetes import client, config, watch
import os
import re
import threading
import yaml


def watch_configmaps():
    while True:
        stream = watch.Watch().stream(v1.list_namespaced_config_map, namespace, timeout_seconds=10)
        for event in stream:
            obj = event["object"]
            obj_dict = obj.to_dict()
            current_config_map_name = obj_dict['metadata']['name']
            if current_config_map_name == config_map_name and event["type"] == 'MODIFIED':
                print("Exiting as configmap was changed")
                os._exit(1)


def decisionmaker(form):
    result = None
    for key1 in form:
        for key2 in rules:
            rule = rules[key2]
            if rule.get('match', 'fqdn') == key1 and re.match(rule['value'], form[key1]):
                print("Matching for %s" % key1)
                if 'return' in rule:
                    result = rule['return']
                    break
                else:
                    print("Missing mcp for %s" % key1)
    return result


kubernetes = False
if 'KUBERNETES_PORT' in os.environ:
    config.load_incluster_config()
elif 'KUBECONFIG' in os.environ:
    config.load_kube_config()

if kubernetes:
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.CoreV1Api()
    try:
        k8sfile = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
        namespace = open(k8sfile, 'r').read() if os.path.exists(k8sfile) else os.environ.get('NAMESPACE', 'default')
        config_map_name = os.environ.get('CONFIG_MAP', 'lighter-rules')
        config_map = v1.read_namespaced_config_map(namespace=namespace, name=config_map_name)
        data = config_map.to_dict().get('data', {})
        if data:
            rules = list(data.values())[0]
            try:
                rules = yaml.safe_load(rules)
            except Exception as e:
                print("Hit %s when reading lighter-rules.yml file" % e)
                os._exit(1)
    except Exception as e:
        if e.status == 404:
            print("Missing configmap %s in namespace %s" % (config_map_name, namespace))
        else:
            print(e)
        rules = {}
    threading.Thread(target=watch_configmaps).start()
elif not os.path.exists("lighter-rules.yml"):
    print("Missing lighter-rules.yml file")
    rules = {}
else:
    with open("lighter-rules.yml") as f:
        try:
            rules = yaml.safe_load(f)
        except Exception as e:
            print("Hit %s when reading lighter-rules.yml file" % e)
            os._exit(1)

if not rules:
    print("Starting without rules")
else:
    print("Using the following rules")
    print(rules)

app = Flask(__name__)
try:
    app.config.from_object('settings')
    config = app.config
except ImportError:
    config = {'PORT': os.environ.get('PORT', 9000)}

debug = config['DEBUG'] if 'DEBUG' in list(config) else False
port = int(config['PORT']) if 'PORT' in list(config) else 9000


@app.route('/', methods=['POST'])
def index():
    """
    entry point
    """
    form = request.get_json()
    data = decisionmaker(form)
    if data is None:
        result = {'result': 'failure', 'reason': "No matching data"}
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
