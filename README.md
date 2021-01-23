# Learning Kubernetes
Exploratory Repo for learning K8s

### Setup

- Get the simple API built for this repo
  - `git clone https://github.com/3digitdev/k8s-learning.git && cd k8s-learning`

---

## Goal 0:  Stop typing `kuberenetes` :confounded:

---

## Goal 1:  Simple API Application  :heavy_check_mark:

Following [This Tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

- Create a Docker image that runs a simple REST API
  - `docker build -t fastapi api/.`
- Build a simple single-node cluster
  - `minikube start`
- Use minikube Docker env
  - `eval $(minikube -p minikube docker-env)`
- Deploy the image to the cluster
  - `kubectl create deployment k8s-fastapi --image=fastapi:latest`
- Verify the app is running
  - `kubectl get pods`
- Expose the app with a Service
  - `kubectl expose deploy/k8s-fastapi --type="NodePort" --port=8080`
- Verify the Service is up
  - `kubectl get service`
- Shortcut for Node port
  - `export NODE_PORT=$(kubectl get svc/k8s-fastapi -o jsonpath="{.spec.ports[0].nodePort}")`
- Ping the API
  - `curl $(minikube ip):$NODE_PORT/hello`
  - Expected response:  `{"message":"Hello World!"}`
- Cleanup
  - `kubectl delete deploy/k8s-fastapi`
  - `kubectl delete svc/k8s-fastapi`
- Verify cleanup
  - `kubectl get pods,deploy,svc`
- Take down the Cluster
  - `minikube delete`

---

## Goal 2:  Goal 1, but with YAML  :heavy_check_mark:

Using [v1.20 API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/)

- Create a Docker image that runs a simple REST API
  - `docker build -t fastapi api/.`
- Build a simple single-node cluster
  - `minikube start`
- Use minikube Docker env
  - `eval $(minikube -p minikube docker-env)`
- Create the deployment for the API, and then expose the Cluster using a Service (via YAML)
  - `kubectl create -f k8s_yml/goal2.yml`
- Shortcut for Node port
  - `export NODE_PORT=$(kubectl get svc/fastapi-svc -o jsonpath="{.spec.ports[0].nodePort}")`
- Ping the API
  - `curl $(minikube ip):$NODE_PORT/hello`
  - Expected response:  `{"message":"Hello World!"}`
- Cleanup
  - `kubectl delete -f k8s_yml/goal2.yml`
- Verify Cleanup
  - `kubectl get pods,deploy,svc`
- Take down the Cluster
  - `minikube delete`

---

## Goal 3:  Add a "Consumer" of the API in a SEPARATE POD that communicates with the API Pod

- Create a Docker image that runs a simple REST API
  - `docker build -t fastapi api/.`
- Create a Docker image that runs a simple API Consumer
  - `docker build -t fastconsumer consumer/.`
- Build a simple single-node cluster
  - `minikube start`
- Use minikube Docker env
  - `eval $(minikube -p minikube docker-env)`
- Create the Deployment for the API, and then expose the Cluster using a Service (via YAML)
  - `kubectl create -f k8s_yml/goal3_api.yml`
- Create the Deployment for the Consumer (via YAML)
  - `kubectl create -f k8s_yml/goal3_consumer.yml`
- Verify the Consumer worked
  - `kubectl logs $(kubectl get pods -l app=fastconsumer_lbl -o jsonpath="{.items[0].metadata.name}")`
  - Should see something like this:
```
$ kubectl logs $(kubectl get pods -l app=fastconsumer_lbl -o jsonpath="{.items[0].metadata.name}")
http://10.100.110.136:8080/hello [1] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [2] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [3] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [4] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [5] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [6] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [7] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [8] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [9] 200: {'message': 'Hello World!'}
http://10.100.110.136:8080/hello [10] 200: {'message': 'Hello World!'}
```
- Cleanup
  - `kubectl delete -f k8s_yml/goal3_api.yml -f k8s_yml/goal3_consumer.yml`
- Verify Cleanup
  - `kubectl get pods,deploy,svc`
- Take down the Cluster
  - `minikube delete`

---

## Goal 4:  Add a Persistent Volume that both API and Consumer can access