# Kubernetes Learning Notes

## Basic Terms

### High Level

[Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/components/)

#### Cluster:
- A group of nodes that represent one large computing instance
- Has a single "master" that manages the Cluster

#### Node:
- [Reference](https://kubernetes.io/docs/concepts/architecture/nodes/)
- A single computing instance in a Cluster.
- This could be a physical machine, or a VM, etc.
- These share the work of running the Pods
  - The Cluster will manage who is running what, shifting resources, balancing, etc.
- A single Node can have multiple Pods running on it

#### Persistent Volumes:
- [Reference](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Since applications shift between Nodes, there's no expectation of storage permanence
- Peristent Volumes are mounted to the Cluster, to give Nodes a shared storage method

### Internals
#### Container:
- A single contained application instance (such as a Docker Container)

#### Pod:
- [Reference](https://kubernetes.io/docs/concepts/workloads/pods/)
- A group of Containers that share the same resources and local network
- **Shared Resources:**
  - Shared storage, as [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
  - Networking, as a unique Cluster IP address
  - Info about how to run each Container (image version, specific ports, etc.)
- Each Pod is tied to a single Node where it was scheduled to
  - Remains there until termination (according to a "restart policy")
- In case of a Node failure, the Pod is replicated across multiple other available Nodes

#### Deployment:
- A group of Pods
- Decides how many Replicas of a single Pod should be running at once
- Manages the Pod(s) inside of it

#### Service:
- [Reference](https://kubernetes.io/docs/concepts/services-networking/service/)
- Defines a logical set of Pods, and a policy on how to access them
- Defined using YAML
- The set of Pods targeted by a Service is determined by a `LabelSelector`
- Exposed in various ways, using `type` in the ServiceSpec:
  - `ClusterIP` (default)
    - Exposes the Services on an internal IP address in the Cluster
    - Service is only reachable INSIDE the Cluster
  - `NodePort`
    - Exposes the Service on the same port of each selected Node in the Cluster
    - Service is reachable with `<NODE_IP>:<NODE_PORT>`
  - `LoadBalancer`
    - Creates an external load balancer on the current cloud
    - Assigns a fixed external IP address to the Service
  - `ExternalName`
    - Exposes the Service at a name defined by the `externalName` ServiceSpec property
    - Requires `kube-dns:1.7+`

--------------------

### Configuration:

#### Ingress:
- [Reference](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- This is an open channel between the outside world and the Cluster
- By default, Clusters have no communication with the outside world
- Multiple methods:
  - Ingress Controller
  - LoadBalancer

#### ConfigMaps:
- [Reference](https://kubernetes.io/docs/concepts/configuration/configmap/)
- A method of setting up environment variables to be used across multiple microservices
- Can be re-used across multiple containers instead of having to set them inside of Dockerfiles
- Store *non-confidential* key-value pairs
- In `kubernetes.yaml`: referenced in `spec.template.spec.containers`, using something like:
```yaml
[...]
env:
- name: APP_NAME            <-- The env variable to store the value in
  valueFrom:
    configMapRef:
      name: sys-app-name    <--  The <name> of the ConfigMap
      key: name             <--  The Key for the key-value-pair
[...]
```

#### Kubernetes Secrets:
- [Reference](https://kubernetes.io/docs/concepts/configuration/secret/)
- Also key-value pairs
- Intended for confidential information
- Stored using Base64
- In `kubernetes.yaml`: referenced in `spec.template.spec.containers`, using something like:
```yaml
[...]
env:
- name: SYSTEM_APP_USERNAME      <-- The env variable to store the value in
  valueFrom:
    secretKeyRef:
      name: sys-app-credentials  <-- the <name> of the Secret
      key: username              <-- The Key for the key-value-pair
- name: SYSTEM_APP_PASSWORD
  valueFrom:
    secretKeyRef:
      name: sys-app-credentials
      key: password
[...]
```

---

## `KUBECTL` Commands

- List resources:
  - `kubectl get <resource>`
- Live-Monitor pods (^C to exit)
  - `kubectl get --watch pods`
- Detailed info:
  - `kubectl describe <resource>`
- Print logs for a Container in a Pod:
  - `kubectl logs <pod_name>`
- Execute a command on a Container in a Pod:
  - `kubectl exec <pod_name> -- <command(s)>`
- Create a depoyment
  - `kubectl create deployment <deploy_name> --image=<image>:<version>`
- Expose a Service
  - `kubectl expose <deployment> --type="<ServiceSpec.Type>" --port=<port>`
- Label a Pod
  - `kubectl label pod <pod_name> <key>=<value>`
- Await a certain status
  - `kubectl wait --for=condition=ready pod -l <label>`
- Build a ConfigMap
  - `kubectl create configmap <name> [OPTS]`
  - **OPTS:**
    - `--from-literal <key>=<value>`  (can do multiple)
    - `--from-file <file>`
    - `--from-env-file <file>`
- Build a Kubernetes Secret
  - `kubectl create secret [TYPE] <name> [OPTS]`
    - **TYPE:**
      - Many types for various purposes like storing docker creds or ssh auth
      - See [Kubernetes Secret Types](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types)
    - **OPTS:**
      - `--from-literal <key>=<value>`  (can do multiple)
      - `--from-file <file>`
      - `--from-env-file <file>`

---

### K8s Object Short Names
```
configmaps............cm
deployments...........deploy
ingresses.............ing
nodes.................no
pods..................po
persistentvolumes.....pv
replicasets...........rs
services..............svc
```

---

### Miscellaneous 
- Get only Pod and store the Pod name as $POD_NAME
  - `export POD_NAME=$(kubectl get pods -l <LABEL> -o jsonpath="{.items[0].metadata.name}")`
- Get a Service and store the NodePort as $NODE_PORT
  - `export NODE_PORT=$(kubectl get svc/<SERVICE_NAME> -o jsonpath="{.spec.ports[0].nodePort}")`
- Bash inside a Pod (`exit` to leave)
  - `kubectl exec -it $POD_NAME -- bash`