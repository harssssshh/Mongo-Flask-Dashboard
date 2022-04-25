# Steps to Install:

### Build Image:
1. Clone the repo.
2.  `docker build -t <image-name> .`
3.  Application expects MongoDB creds. to be there using env. variables.
4. Start the container :-
` docker run --name os-dashboard -e DB_NAME=<Your-Database-Name> -e DB_USERNAME=<Your-Username> -e DB_PASS=<Your-Password> -e CLUSTER_NAME=<Cluster-Name (xxxxxx.xxx.mongodb.net)> --network=host -it <image-name>`

**Replace the values in <>**
**Application runs by defauly on Port 5000, if port that port is consumed on host replace --network=host with -p  YOUR-PORT:5000**


### Deploying On Kubernetes

1. Inside Deployment Directory, First create a secret using
` kubectl create secret generic dbcreds --from-literal=DB_NAME=<Your-DB-Name> --from-literal=DB_PASS=<Your-DB-Pass> --from-literal=DB_USERNAME=<Your-DB-Username> --from-literal=CLUSTER_NAME=<Cluster-Name (xxxxxx.xxx.mongodb.net)> --dry-run=client -o yaml > secret.yaml`

2. Create a namespace: `kubectl create ns dashboard`
3. `kubectl apply -n dashboard -f .`

	** Replace the ClusterIP with NodePort if you don't  have ingress controller in service.yaml **

