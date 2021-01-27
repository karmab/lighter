This repo contains sample code for a POC of providing specific ignition from an Openshift Cluster to nodes requesting them and 
matching some of the hardware data they send to identify themselves, such as:

- mac
- ip
- fqdn

```
curl -X POST -H "Content-Type: application/json"  -d "{\"mac\": \"XXX\"}" 127.0.0.1:9000
```
