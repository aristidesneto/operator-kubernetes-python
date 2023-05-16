from flask import Flask, request, jsonify
import os

from kubernetes import client, config
from kubernetes.client.rest import ApiException

app = Flask(__name__)

if 'KUBERNETES_PORT' in os.environ:
    config.load_incluster_config()
else:
    config.load_kube_config()

@app.route('/api/create', methods=["POST"])
def create():
    data = request.get_json()
    # Secret template 
    secret = {"apiVersion": "v1", "kind": "Secret", "metadata": {"name": data['name'], "namespace": data['namespace']}, "type": "Opaque", "data": data['data']}

    # Objeto kubernetes API
    api = client.CoreV1Api()
    
    obj_secret = None

    # Criar secret
    try:
        obj_secret = api.read_namespaced_secret(data['name'], data['namespace'])
    except ApiException as e:
        print(e)
    
    if obj_secret:
        obj_delete = api.delete_namespaced_secret(data['name'], data['namespace'])
        print(f'Secret "{obj_delete.details.name}" deleted')
    
    obj = api.create_namespaced_secret(data['namespace'], secret)
    print(f"Secret {obj.metadata.namespace}/{obj.metadata.name} created")

    return '', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")