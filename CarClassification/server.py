from kubernetes import client, config
from kubernetes.client.rest import ApiException
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
#app.run(debug = True)
api_instance = client.BatchV1Api()
print(api_instance)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []
    print("hey")
    # your code here
    ret=v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        #pods.append({"node" : i.spec.node_name, "ip" : i.status.pod_ip, "namespace" : i.metadata.namespace, "name" : i.metadata.name, "status":pod.status.phase})
        pods.append({"name" : i.metadata.name,"ip" : i.status.pod_ip,"namespace" : i.metadata.namespace,"node" : i.spec.node_name,  "status":i.status.phase})

    print(pods)
    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here
    namespace = "free-service"
    with open(path.join(path.dirname(__file__), "free-service-job.yaml")) as f:
    # Create an instance of the API class
        dep=yaml.safe_load(f)
        print(dep)
        try:
            api_response = api_instance.create_namespaced_job(namespace=namespace,body=dep)
            print(api_response)
        except ApiException as e:
            print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)
    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    body = request.get_json(force=True)
    namespace = "default"
    with open(path.join(path.dirname(__file__),"default.yaml")) as f:
        dep=yaml.safe_load(f)
        resp = api_instance.create_namespaced_job(namespace=namespace,body=dep)
    return "success"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
