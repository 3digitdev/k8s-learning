# Learning Kubernetes
Exploratory Repo for learning K8s

### Setup

- Get the simple API built for this repo
  - `git clone https://github.com/3digitdev/k8s-learning.git && cd k8s-learning`

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
  - `export NODE_PORT=$(kubectl get svc/k8s-fastapi -o go-template='{{(index .spec.ports 0).nodePort}}')`
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
- Create the deployment from and then expose the Cluster using a Service (via YAML)
  - `kubectl create -f k8s_yml/goal2.yml`
- Shortcut for Node port
  - `export NODE_PORT=$(kubectl get svc/fastapi-svc -o go-template='{{(index .spec.ports 0).nodePort}}')`
- Ping the API
  - `curl $(minikube ip):$NODE_PORT/hello`
  - Expected response:  `{"message":"Hello World!"}`
- Cleanup
  - `kubectl delete -f k8s_yml/goal2/service.yml -f k8s_yml/goal2/deployment.yml`
- Verify Cleanup
  - `kubectl get pods,deploy,svc`
- Take down the Cluster
  - `minikube delete`

---

## Goal 3:  Goal 1 w/ second Pod that pings the API

---

## Goal 4:  Goal 3, but with YAML

---

## Goal 5:  Stop typing `kuberenetes` :confounded: