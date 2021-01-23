# Learning Kubernetes
Exploratory Repo for learning K8s

## Goal 1:  Simple API Application  :heavy_check_mark:

Following [This Tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

- Create a simple API with Python
  - `git clone https://github.com/3digitdev/k8s-learning.git`
- Create a Docker image that runs it
  - `cd k8s-learning && docker build -t fastapi .`
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

---

## Goal 2:  Goal 1, but with YAML

---

## Goal 3:  Goal 1 w/ second Pod that pings the API

---

## Goal 4:  Goal 3, but with YAML

---

## Goal 5:  Stop typing `kuberenetes` :confounded: