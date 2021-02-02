This repo contains sample code for a POC of providing specific ignition (or arbitrary data) from an Openshift Cluster to nodes requesting them and 
matching some of the hardware data they send to identify themselves, such as:

- mac
- ip
- fqdn
- whatever key you want to use

The component can either be run in a standalone mode or on kubernetes

## Client side 

The client needs to send a json POST request providing key-values pair. For
instance

```
curl -X POST -H "Content-Type: application/json"  -d "{\"mac\": \"XXX\"}" 127.0.0.1:9000
```

A json response will be sent which will contain
- result set to either success or failure
- reason if any failure
- data if any match, containing the url of the ignition file to use for this node


## Running

### Configuration

A file containing the rules needs to be provided. In dev mode, the file lighter-rules.yml is used.

On Kubernetes/Openshift, the configmap lighter-rules in the lighter namespace is parsed. It can be created from a file
using the following:

```
kubectl create configmap lighter-rules --from-file=rules=lighter-rules.yml -n lighter
```

### dev mode

You will need python3 and [kubernetes client python](https://github.com/kubernetes-client/python) that you can either install with pip or your favorite package manager.

```
python3 main.py
```

### standalone

You can run against an existing cluster after setting your KUBECONFIG env variable with the following invocation

```
podman run -v $(dirname $KUBECONFIG):/kubeconfig -e KUBECONFIG=/kubeconfig/kubeconfig --rm -it karmab/lighter
```

### In Openshift/Kubernetes

```
kubectl create -f deployment.yml
```
