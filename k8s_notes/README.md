# Kubernetes Tutorial

## Table of Content

- [Kubernetes Tutorial](#kubernetes-tutorial)
  - [Table of Content](#table-of-content)
  - [Kubernetes Introduction](#kubernetes-introduction)
  - [K8s Concepts And Architecture](#k8s-concepts-and-architecture)
  - [Installation of Kubernetes \[Locally\]](#installation-of-kubernetes-locally)
    - [Install Kubectl](#install-kubectl)
    - [Install Minikube](#install-minikube)
    - [Starting Minikube](#starting-minikube)
    - [With Docker Backend](#with-docker-backend)
    - [With HyperKit Backend](#with-hyperkit-backend)
  - [Objects In K8s](#objects-in-k8s)
    - [Pod Object](#pod-object)
    - [Node Object](#node-object)
    - [Namespace Object](#namespace-object)
    - [Deployment Object](#deployment-object)
    - [ReplicaSet](#replicaset)
    - [Service](#service)
    - [Job](#job)
    - [StatefulSet](#statefulset)
    - [DaemonSet](#daemonset)
      - [Deployment \[Imperative Approach\]](#deployment-imperative-approach)
      - [View Pods](#view-pods)
      - [View Specific Pod Details](#view-specific-pod-details)
      - [Get Logs of A K8s Pod](#get-logs-of-a-k8s-pod)
      - [Execute Commands In A Container \[kubectl exec command\]](#execute-commands-in-a-container-kubectl-exec-command)
      - [Access One of The Containers In The Pod](#access-one-of-the-containers-in-the-pod)
      - [Expose A Deployment (Create A Service)](#expose-a-deployment-create-a-service)
      - [Scaling Deployments](#scaling-deployments)
      - [Updating Deployments \[With Docker Images\]](#updating-deployments-with-docker-images)
      - [Rollback Deployments](#rollback-deployments)
  - [Imperative Object Configuration \[Using Config Files\]](#imperative-object-configuration-using-config-files)
    - [Deployment Config File](#deployment-config-file)
    - [Create Deployment](#create-deployment)
    - [Service Config File](#service-config-file)
    - [Updating The Config File](#updating-the-config-file)
    - [Delete Resources In A Config File](#delete-resources-in-a-config-file)
    - [Create Multiple Objects In A Single File](#create-multiple-objects-in-a-single-file)
    - [Add Liveness Probes](#add-liveness-probes)
    - [Image Pull Policy](#image-pull-policy)
    - [Service Object](#service-object)
      - [Create A Service](#create-a-service)
      - [Describe A Service](#describe-a-service)
      - [Port Forwarding A Service](#port-forwarding-a-service)
      - [List All The Resources In A K8s Cluster](#list-all-the-resources-in-a-k8s-cluster)
      - [Node Port](#node-port)
      - [Load Balancer](#load-balancer)
    - [Environment Variables](#environment-variables)
      - [Retrieve Environment Variables In A Pod](#retrieve-environment-variables-in-a-pod)
    - [Secret Config File](#secret-config-file)
    - [Namespace](#namespace)
  - [Data And Volumes](#data-and-volumes)
    - [EmptyDir](#emptydir)
    - [HostPath](#hostpath)
  - [Networking](#networking)
    - [Pod Internal Communication](#pod-internal-communication)
      - [Multiple Containers In One Pods](#multiple-containers-in-one-pods)
    - [Pod to pod connection](#pod-to-pod-connection)
      - [1. Manually Copying The Cluster IP of The Pod](#1-manually-copying-the-cluster-ip-of-the-pod)
      - [2. Auto Generated Environment Variables](#2-auto-generated-environment-variables)
      - [3. DNS For Pod-Pod Communication](#3-dns-for-pod-pod-communication)
    - [To Do](#to-do)
  - [Miscellaneous Commands](#miscellaneous-commands)
  - [K8s Context](#k8s-context)
    - [Get Available Contexts](#get-available-contexts)
    - [Get Switch Contexts](#get-switch-contexts)
    - [Verify Current Contexts](#verify-current-contexts)

## Kubernetes Introduction

```text
- Kubernetes is an open-source container orchestration system for automating deployment, scaling, and management of containerized applications.
- It is a portable, extensible, and scalable platform that can be used on-premises or in the cloud.

Advantages
----------
1. Automated deployment and scaling: Kubernetes can automatically deploy and scale containerized applications based on demand. This helps to ensure that applications are always available and running at peak performance.

2. Self-healing: Kubernetes can automatically restart or replace containers that fail. This helps to ensure that applications are always up and running, even if there are individual failures.

3. Load balancing: Kubernetes can automatically distribute traffic across multiple containers. This helps to ensure that applications are always responsive, even if there is a high volume of traffic.

4. Storage orchestration: Kubernetes can automatically mount storage volumes to containers. This helps to simplify the management of persistent data.

5. Multi-cloud support: Kubernetes can be run on a variety of cloud platforms, including AWS, Azure, and Google Cloud Platform. This makes it easy to deploy and manage applications across multiple clouds.

Additional benefits include:
- Portability: Kubernetes is a portable platform, which means that applications can be deployed and managed on a variety of different environments. This makes it easy to move applications between different clouds or on-premises environments.

- Flexibility: Kubernetes is a flexible platform, which means that it can be used to deploy a wide variety of applications. This makes it a good choice for businesses that need to deploy a variety of different types of applications.

- Cost savings: Kubernetes can help to save businesses money by automating the deployment and scaling of applications. This can help to reduce the need for manual intervention, which can save time and money.
```

## K8s Concepts And Architecture

```text
Cluster
-------
- A Kubernetes cluster is a group of machines that are running Kubernetes. Each machine in a cluster is called a node.

Pods
----
- A pod is the smallest unit of deployment in Kubernetes. A pod is a group of one or more containers that are scheduled to run on the same node.

Deployments
-----------
- A deployment is a way to manage the lifecycle of a pod. A deployment can be used to create, update, and delete pods.

ReplicaSets
-----------
- A replica set is a way to ensure that a certain number of pods are running at all times. A replica set will create new pods if any pods in the set fail.

StatefulSets
------------
- A StatefulSet is a way to manage stateful applications in Kubernetes. A StatefulSet ensures that pods are created in a specific order and that they are assigned unique IDs.

Services
--------
- A service is a way to expose a pod or set of pods to the outside world. A service can be used to load balance traffic across pods or to provide access to pods that are running on different nodes.

Volumes
-------
- A volume is a way to store data in Kubernetes. Volumes can be used to store data that is shared between pods or to store data that is persistent across pod restarts.



Master Node
-----------
- This is a node that runs the Kubernetes control plane. The control plane is responsible for managing the cluster, including scheduling pods, managing resources, and maintaining the cluster state.

Control Plane
-------------
- The control plane is composed of a number of components, including:
1. API server: The API server is the main entry point for interacting with Kubernetes. It exposes a RESTful API that can be used to manage the cluster.

2. Scheduler: The scheduler is responsible for scheduling pods onto worker nodes. It takes into account the resources available on each node and the requirements of the pods when making scheduling decisions.

3. Controller manager: The controller manager is responsible for managing the lifecycle of pods and services. It ensures that pods are created and deleted as needed and that services are updated when pods are added or removed.

Worker Nodes
------------
- The worker nodes are responsible for running pods and services. They each run a kubelet process, which is responsible for interacting with the control plane and managing the pods that are running on the node.

Kubelet
-------
- The kubelet is a process that runs on each node and is responsible for managing the pods that are running on that node.


Proxy
-----
In Kubernetes architecture, a proxy is a component that is responsible for routing traffic to pods. There are two types of proxies in Kubernetes:

- kube-proxy: This is the default proxy in Kubernetes. It is a network proxy that runs on each node in the cluster. kube-proxy maintains network rules on nodes that allow network communication to pods from network sessions inside or outside of the cluster.

- Ingress controller: An ingress controller is a proxy that is responsible for routing traffic to pods that are exposed through an ingress resource. Ingress resources are used to expose HTTP and HTTPS services to the outside world.


In general, `proxies` are used for more basic tasks, such as routing traffic to pods while `Services` are used for more complex tasks, such as exposing pods to the outside world and load balancing traffic across pods.
```

## Installation of Kubernetes [Locally]

### Install Kubectl

- Check [this](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/#install-with-homebrew-on-macos) for updated information.

```bash
# Install with Homebrew on macOS
brew install kubectl

# OR
brew install kubernetes-cli

# Test to ensure the version you installed is up-to-date:
kubectl version --client

# Verify kubectl configuration
kubectl cluster-info

# For more commands
kubectl --help
```

### Install Minikube

- Check [this](https://minikube.sigs.k8s.io/docs/start/) for updated information.

```bash
# Install with Homebrew on macOS
brew install minikube

# If which minikube fails after installation via brew, you may have to
# remove the old minikube links and link the newly installed binary:
brew unlink minikube
brew link minikube

# Start your cluster
minikube start

# If you already have kubectl installed, you can now use
# it to access your new cluster:
kubectl get pods -A

# Launch the minikube dashboard
minikube dashboard

# For more commands
minikube --help
```

### Starting Minikube

### With Docker Backend

```sh
minikube start --driver=docker --cpus=4 --memory=4096MB --disk-size=10GB --nodes=3
```

### With HyperKit Backend

```bash
minikube start --driver=hyperkit --cpus=4 --memory=4096MB --disk-size=10GB --nodes=3
```

```text
minikube start              # Launch minikube
  --driver=hyperkit         # Use the hyperkit driver for virtualization (on macOS).
  --cpus=4                  # Set up a VM with 4 CPU cores
  --memory=4096MB           # VM with 4GB of RAM
  --disk-size=10GB          # VM with 10GB disk.
  --nodes=3                 # k8s cluster with 3 nodes within that VM.
```

## Objects In K8s

### Pod Object

```text
- A pod is the smallest and most basic unit of deployment.

- It represents a single instance of a running process in your cluster.

- A Pod can contain one or more containers (like Docker containers) that are tightly coupled and share resources like network and storage.

- Pods are considered to be ephemeral and disposable. If a pod fails or needs to be rescheduled due to node failures or scaling events, a new pod can be created to replace it.
```

```sh
# List all pods in the default namespace
kubectl get pods

# List all pods in the specified namespace
kubectl get pods -n <namespace>
# e.g., kubectl get pods -n staging

# Describe a specific pod
kubectl describe pod <pod-name>
# e.g., kubectl describe pod my-pod

# Get detailed information about a pod
kubectl get pod <pod-name> -o yaml
# e.g., kubectl get pod my-pod -o yaml

# Get logs of a specific pod
kubectl logs <pod-name>
# e.g., kubectl logs my-pod

# Get events related to a specific pod
kubectl get events --field-selector involvedObject.name=<pod-name>
# e.g., kubectl get events --field-selector involvedObject.name=my-pod

# Delete a specific pod
kubectl delete pod <pod-name>
# e.g., kubectl delete pod my-pod
```

### Node Object

```text
- It's a worker machine in Kubernetes. It can be a physical or virtual machine.

- The Kubernetes control plane manages the nodes, and the pods run on these nodes.
```

### Namespace Object

```text
- It's a way to organize and isolate resources within a Kubernetes cluster.

- It can be thought of as a virtual cluster within your physical cluster, allowing multiple teams or projects to share the same underlying infrastructure without interfering with each other.
```

```sh
# List all namespaces
kubectl get namespaces

# Create a new namespace
kubectl create namespace <namespace-name>
# e.g., kubectl create namespace staging

# Describe a specific namespace
kubectl describe namespace <namespace-name>
# e.g., kubectl describe namespace staging

# Delete a namespace
kubectl delete namespace <namespace-name>
# e.g., kubectl delete namespace staging

# List all resources in a namespace
kubectl get all -n <namespace-name>
# e.g., kubectl get all -n staging
```

### Deployment Object

```text
- It's a higher-level object that manages a set of identical Pods.

- Deployments ensure that a specified number of Pod "replicas" are running at any given time.

- If a Pod fails, the Deployment will automatically create a new one to maintain the desired state.

- Deployments also handle rolling updates and rollbacks of your application.

- e.g. a web application deployment that consists of multiple instances of a web server that runs continuously unlike a Job that runs once until completion.
```

```sh
# List all deployments
kubectl get deployments

# List all deployments in a specific namespace
kubectl get deployments -n <namespace-name>
# e.g., kubectl get deployments -n staging

# Describe a specific deployment
kubectl describe deployment <deployment-name>
# e.g., kubectl describe deployment my-deployment

# Get detailed information about a deployment
kubectl get deployment <deployment-name> -o yaml
# e.g., kubectl get deployment my-deployment -o yaml

# Delete a specific deployment
kubectl delete deployment <deployment-name>
# e.g., kubectl delete deployment my-deployment
```

### ReplicaSet

```text
- It's the underlying mechanism used by Deployments to maintain the desired number of Pod replicas.
- You typically don't interact with ReplicaSets directly as a user; Deployments manage them for you.
```

### Service

```text
- It provides a stable IP address and DNS name to access a set of Pods.

- Services act as an abstraction layer, allowing you to access your application without needing to know the specific IP addresses of the individual Pods, which can be dynamic.

- Common service types include:
  - ClusterIP (internal access)
  - NodePort (access via each node's IP and a port)
  - LoadBalancer (external access via a cloud provider's load balancer)
```

```sh
# List all services
kubectl get services

# List all services in a specific namespace
kubectl get services -n <namespace-name>
# e.g., kubectl get services -n staging

# Describe a specific service
kubectl describe service <service-name>
# e.g., kubectl describe service my-service

# Get detailed information about a service
kubectl get service <service-name> -o yaml
# e.g., kubectl get service my-service -o yaml

# Delete a specific service
kubectl delete service <service-name>
# e.g., kubectl delete service my-service
```

### Job

```text
- It represents a finite task that runs to completion.

- Unlike Deployments that ensure continuous running, Jobs are for batch-oriented workloads that have a defined start and end.

- e.g. a data processing task or a one-time setup script.
```

```sh
# List all jobs
kubectl get jobs

# List all jobs in a specific namespace
kubectl get jobs -n <namespace-name>
# e.g., kubectl get jobs -n staging

# Describe a specific job
kubectl describe job <job-name>
# e.g., kubectl describe job my-job

# Delete a specific job
kubectl delete job <job-name>
# e.g., kubectl delete job my-job
```

### StatefulSet

```text
- It's similar to Deployments, but designed for stateful applications that require stable, persistent storage and unique network identifiers for their Pods.

- Examples include databases like PostgreSQL or Cassandra.
```

```sh
# List all statefulsets
kubectl get statefulsets

# List all statefulsets in a specific namespace
kubectl get statefulsets -n <namespace-name>
# e.g., kubectl get statefulsets -n staging

# Describe a specific statefulset
kubectl describe statefulset <statefulset-name>
# e.g., kubectl describe statefulset my-statefulset

# Delete a specific statefulset
kubectl delete statefulset <statefulset-name>
# e.g., kubectl delete statefulset my-statefulset
```

### DaemonSet

```text
- It ensures that a copy of a Pod runs on each Node in the cluster.

- DaemonSets are useful for deploying cluster-level agents, such as log collectors (like Fluentd or Logstash) or monitoring agents.
```

#### Deployment [Imperative Approach]

```bash
# 1. Build an image and push to a Docker repository like Dockerhub.
docker build -t <image_name:tag> -f <Dockerfile> <./path_to_file>
# e.g.
docker build -t chineidu/other_service:v2 -f other/Dockerfile ./other/Dockerfile

# 2. Start the K8s cluster.
minikube start

# 3. Create a deployment object using `kubectl`.
kubectl create deployment <deployment_name> --image=<image_name:tag>
# e.g.
# Note: underscores are NOT supported.
kubectl create deployment first-deployment --image=chineidu/other_service:v2

# List all the created deployments in your K8s cluster.
kubectl get deployments

# Delete a K8s deployment.
kubectl delete deployment <deployment_name>

# Check the status of the deployment using the dashboard
minikube dashboard
```

#### View Pods

```bash
# List all the running pods in your K8s cluster.
kubectl get pods

# List all pods and monitor live status
kubectl get pods --watch
```

#### View Specific Pod Details

```bash
# List all the running pods in your K8s cluster.
kubectl describe pod <pod-name>
# e.g.
 kubectl describe pods second-app-7d94996d68-bqqh4
```

#### Get Logs of A K8s Pod

```text
- It's used to view the logs for a Kubernetes pod. i.e. the logs can be used to troubleshoot problems with pods and to understand the behavior of applications running in pods.

Some additional flags that you can use with the `kubectl logs` command:
--follow: This flag will cause the command to follow the logs for the pod and update the output accordingly.
--tail: This flag can be used to specify the number of lines of logs that will be displayed.
--since: This flag can be used to specify the time since which the logs will be displayed.
```

```bash
kubectl logs <pod-name>

# Show the last 5 logs
kubectl logs second-app-6695467d49-bwhgg --tail=5

# Show the logs within the last 10 seconds
kubectl logs second-app-6695467d49-bwhgg --since=10s

# Specify if the logs should be streamed.
kubectl logs second-app-6695467d49-bwhgg --follow=true

# Show the logs of a specific container
kubectl logs <pod-name> -c <container-name> -n <namespace>

# For more commands:
kubectl logs --help
```

#### Execute Commands In A Container [kubectl exec command]

```text
- The `kubectl exec` command is used to execute commands in a Kubernetes pod.
- This can be used to troubleshoot problems with pods, to debug applications running in pods, or to perform other tasks that require access to the container's shell.
- It can also be used to execute commands interactively using the `-it` flag.
```

```bash
# Syntax
kubectl exec <pod-name> -- <command>

# List all the files in a pod
kubectl exec second-app-6695467d49-bwhgg -- ls

# Interactive command
kubectl exec -it second-app-6695467d49-bwhgg -- bash

# For more commands:
kubectl exec --help
```

#### Access One of The Containers In The Pod

```bash
# To access one of the containers in the pod, enter the following command:
kubectl exec -it <pod_name> -c <container_name> -- <command>
kubectl exec -it second-app-6695467d49-bwhgg -c mongo -- bash
```

#### Expose A Deployment (Create A Service)

```text
- For the deployment to be accessed by the outside world, it has to be exposed as a `service`.
```

```bash
# Expose a K8s resource, such as a pod, deployment, or replica set, as a service.
# The service will be created in the default namespace, unless a different namespace is specified.
kubectl expose <resource> [options]
# For deployment, it'll look like this
kubectl expose deployment <deployment_name> --type=[ClusterIP|NodePort|LoadBalancer] --port=$PORT
# OR
kubectl expose deployment <deployment_name> --type [ClusterIP|NodePort|LoadBalancer] --port $PORT
kubectl expose deployment first-deployment --type=LoadBalancer --port=6060

# List all the created services
kubectl get services

# To display the external IP for local setup
minikube service <service_name>
# e.g.
minikube service first-deployment
```

#### Scaling Deployments

```bash
# Scale a deployment. replicas is the number of pods
kubectl scale deployments <deployment-name> --replicas=<number_of_replicas>

# e.g. Scale UP
kubectl scale deployment first-deployment --replicas=3
# e.g. Scale DOWN
kubectl scale deployment first-deployment --replicas=1
```

#### Updating Deployments [With Docker Images]

```text
- This is used to update a K8s deployment when there are changes to the source code or Docker image(s).

Steps
-----
1. Rebuild the Docker image and push the image to a Docker repository.
2. Update the image on the K8s deployment.
3. Check the status of the deployment.
   - it shows the current state of the rollout, including the number of new replicas that have been created, the number of old replicas that have been terminated, and the number of available replicas.

```

```bash
# Update the image on K8s
kubectl set image deployments/<deployment-name> <container-name>=<new-image>:<tag>
kubectl set image deployments/first-deployment mlops=chineidu/mlops:v3

# Check deployment status
kubectl rollout status deployment/<deployment-name>
# e.g.
kubectl rollout status deployment/first-deployment

# You can also `watch` the status of a rollout as it progresses.
kubectl rollout status deployment/first-deployment --watch
```

#### Rollback Deployments

```bash
# Rollback to the previous deployment
kubectl rollout undo deployment/<deployment-name>
# e.g.
kubectl rollout undo deployment/first-deployment

# Display the deployment history
kubectl rollout history deployment/<deployment-name>
# e.g.
kubectl rollout history deployment/first-deployment

# View A Specific Revision
kubectl rollout history deployment/<deployment-name> --revision=<revision_num>
kubectl rollout history deployment/my-app --revision=2

# Rollback to a specific version
kubectl rollout undo deployment/my-app --to-revision=2
```

## Imperative Object Configuration [Using Config Files]

- Check the [docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/)
- K8s API [docs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/).

```text
- In imperative object configuration, the kubectl command specifies the operation (create, replace, etc.), optional flags and at least one file name.
- The file specified must contain a full definition of the object in YAML or JSON format.
```

### Deployment Config File

- More examples can be found [here](https://codefresh.io/learn/software-deployment/kubernetes-deployment-yaml/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80

```

```text
- This deployment shown above will create 3 replicas of a pod with the `nginx` image.
- The pods will be labeled with the app: nginx label, and they will be exposed on port 80.

Detailed Explanation
--------------------
- apiVersion: specifies the Kubernetes API version that the deployment is using.
- kind: specifies the type of Kubernetes object that the deployment is creating.
- metadata: contains the metadata for the deployment, such as its name and labels.
- spec: specifies the configuration for the deployment, such as the number of replicas and the pod template.
- selector: specifies the labels that the pods in the deployment should be labeled with.
- template: specifies the template for the pods in the deployment.
- containers: specifies the containers that should be included in the pods.
```

### Create Deployment

```bash
# To create the resources specified in the config file
kubectl apply -f <filename.yaml>
# OR
kubectl apply -f=<filename.yaml>
# e.g.
kubectl apply -f deployment.yaml
```

### Service Config File

- An example `service` object config is shown below.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: second-app
  ports:
  - port: 8000
    targetPort: 8000
  type: LoadBalancer

```

### Updating The Config File

```text
- Changes can be made and updated on the config file by saving the file and running the command:

$ kubectl apply -f filename.yaml
```

### Delete Resources In A Config File

```text
Resources can be deleted using the:
1. Imperative approach. i.e. using ONLY the CLI.
2. Imperative object approach. i.e. using a config file
```

```bash
# Using ONLY CLI
kubectl delete <resource_type> <resource_name>
# e.g.
kubectl delete deployment my-app

# Using confile file and CLI
# Point to the fil(e) and delete all the resources in the file(s):
kubectl delete -f <filename1.yaml> -f <filename2.yaml>
# e.g.
kubectl delete -f deployment.yaml

# Delete a resource using a label
kubectl delete <resource_type> -l <label_key>:<label_value>
kubectl delete services,deployments -l app:second-app
```

### Create Multiple Objects In A Single File

```text
- Multiple objects and resources can be defined in a single file.
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: second-app
  ports:
  - port: 8000
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: second-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: second-app
  template:
    metadata:
      labels:
        app: second-app
    spec:
      containers:
        - name: second-app
          image: chineidu/mlops:v3
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
          ports:
            - containerPort: 8000

```

### Add Liveness Probes

```text
- A liveness probe is a mechanism in Kubernetes that ensures that an application running in a container is alive and operational.
- If the liveness probe detects an unhealthy state, then Kubernetes kills the container and tries to redeploy it.
- The liveness probe is configured in the `spec.containers.livenessProbe` attribute of the pod configuration.

The liveness probe is configured with a number of parameters, including:
* initialDelaySeconds: The number of seconds to wait before the first liveness probe is executed.
* periodSeconds: The number of seconds between liveness probes.
* failureThreshold: The number of consecutive liveness probes that must fail before the container is killed.
* successThreshold: The number of consecutive liveness probes that must succeed before the container is considered healthy.

```

```yaml
apiVersion: apps/v1
kind: Deployment
... # I shortened the config file

    spec:
      containers:
        - name: second-app
          image: chineidu/mlops:v3
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
          ports:
            - containerPort: 8000
          livenessProbe:
            httpGet:
              path: /
              port: 8000
            periodSeconds: 10
            initialDelaySeconds: 5
```

### Image Pull Policy

```text
- Kubernetes image pull policy is a configuration that specifies how Kubernetes will pull images when a pod is created or updated.

Possible values for image pull policy:
1. IfNotPresent: Kubernetes will only pull the image if it is not already present on the node.
2. Always: Kubernetes will always pull the image, even if it is already present on the node.
3. Never: Kubernetes will never pull the image, even if it is not present on the node.

- The default value for image pull policy is `IfNotPresent`.
- This means that Kubernetes will only pull the image if it's not already present on the node.
- If the image is already present on the node, Kubernetes will use the locally stored image.
```

### Service Object

#### Create A Service

```bash
# Expose a K8s resource, such as a pod, deployment, or replica set, as a service.
kubectl expose deployment <deployment_name> --type [ClusterIP|NodePort|LoadBalancer] --port $PORT
# e.g.
kubectl expose deployment first-deployment --type=LoadBalancer --port=6060

# List all the created services
kubectl get services

# To display the external IP for local setup
minikube service <service_name>
# e.g.
minikube service first-deployment
```

#### Describe A Service

```text
- The kubectl describe command is used to display detailed information about a Kubernetes resource.
- The resource can be a pod, a deployment, a service, or any other type of Kubernetes resource.
- The kubectl describe command takes the name of the resource as an argument.
```

```bash
# For example, the following command will display detailed information about the pod named nginx-pod:
kubectl describe service <service-name>
# e.g.
kubectl describe service backend
```

#### Port Forwarding A Service

```sh
kubectl port-forward <service-name> <local-port>:<service-port> -n <your-namespace>

# e.g.
kubectl port-forward service/backend 8080:80
```

#### List All The Resources In A K8s Cluster

```text
- This is used to list all of the resources in a Kubernetes cluster.
- The resources can be pods, deployments, services, stateful sets, and any other type of Kubernetes resource.
```

```bash
kubectl get all
```

#### Node Port

```text
Node Port
---------
- This is a type of service that exposes a service on a specific port on each node in the cluster.
- This allows external users to access the service without having to use a load balancer.
- NodePorts are useful for exposing services that need to be accessed by external users, but do not need to be load balanced. e.g. you might use a NodePort to expose a web application that is only used by a small number of users.
- NodePorts are configured in the spec.ports section of the service manifest.
- The nodePort field specifies the port that the service will be exposed on each node.
- The nodePort field must be a value in the range `30000-32767`.
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: second-app
  type: NodePort # nodeport
  ports:
    - port: 8000
      targetPort: 8000
      nodePort: 30000 # nodeport
```

#### Load Balancer

```text
Load Balancer
-------------
- A Kubernetes load balancer is a service that distributes traffic across multiple pods.
- This can help to improve the performance and availability of your applications.
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: second-app
  type: LoadBalancer
  ports:
    - port: 8000
      targetPort: 8000
```

```bash
# Method 1. # Expose a K8s resource, such as a pod, deployment, or replica set, as a service.
export PORT=8000
kubectl expose deployment <deployment_name> --type=[ClusterIP|NodePort|LoadBalancer] --port=$PORT
kubectl expose deployment first-deployment --type=LoadBalancer --port=$PORT

# Method 2.
kubectl apply -f <filename.yaml>
# e.g. This creates and exposes the service object in the specified yaml file.
kubectl apply -f main_config.yaml
```

### Environment Variables

```yaml

# Load the secrets as env vars
apiVersion: apps/v1
kind: Deployment
metadata:
  name: second-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app-with-db
  template:
    metadata:
      labels:
        app: app-with-db

    spec:
      containers:
        - name: mongo
          image: mongo:7.0-rc
          imagePullPolicy: IfNotPresent # default
          resources:
            limits:
              memory: "256Mi"
              cpu: "250m"
          ports:
            - containerPort: 27017
          env:
            - name: MONGO_INITDB_ROOT_USERNAME
              value: neidu
            - name: MONGO_INITDB_ROOT_PASSWORD
              value: password

```

#### Retrieve Environment Variables In A Pod

```sh
# 1. ssh into the pod
kubectl exec -it <pod-name> -n <namespace> -- <command>
# e.g.
kubectl exec -it app-1-c86cf468d-89zw4 -n development -- sh

# 2. Once you're in the shell of the pod, view all the env vars
# by running the command:
printenv
```

### Secret Config File

- For more info, check the [official docs](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-config-file/)
- [Blog post](https://www.mirantis.com/blog/cloud-native-5-minutes-at-a-time-using-kubernetes-secrets-with-environment-variables-and-volume-mounts/)

```text
- The secret config file below defines two keys: USERNAME and PASSWORD.
- The values of these keys MUST be base64-encoded strings.

Usage
-----
- After creating the secrets file, you need to apply it with the `kubectl apply` command.
```

```bash
# Generate base64 encoded strings
echo -n "neidu" | base64
# output: bmVpZHU=

echo -n "password" | base64
# output: cGFzc3dvcmQ=
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: bmVpZHU=
  password: cGFzc3dvcmQ=

---
# Load the secrets as env vars
spec:
  containers:
    - name: app-with-db
      image: chineidu/other_service:v1
      imagePullPolicy: IfNotPresent
      resources:
        limits:
          memory: "512Mi"
          cpu: "500m"
      ports:
        - containerPort: 6060
      env:
        - name: USERNAME
          valueFrom:
            secretKeyRef:
              name: my-secret # from secrets.metadata.name
              key: username
        - name: PASSWORD
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
```

### Namespace

```text
- A namespace in Kubernetes is a logical grouping of resources.
- Namespaces help organize Kubernetes resources for various purposes, such as:
- Isolating resources: It isolates resources, ensuring changes in one namespace don't affect others, aiding security and facilitating management of resources for different teams or projects.
- Managing permissions: It's used to manage permissions for resources. This can be helpful for ensuring that only authorized users have access to certain resources.
- Enforcing naming conventions: It's used to enforce naming conventions for resources. This can help to prevent naming conflicts and to make it easier to find and manage resources.

Usage:
------
# Method 1.
$ kubectl create namespace <namespace-name>

# Method 2.
From a config file
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-db-configmap
  namespace: my-namespace # assign a namespace
data:
  mysqlservice.database
```

```bash
# View the available namespaces
kubectl get namespaces

# 1. Create namespace
kubectl create namespace <namespace-name>

# 2. Create from a file
kubectl create -f filename.yaml
# OR
kubectl apply -f filename.yaml

# 3. Create from a file and CLI.
# If the config does NOT already have a namespace.
kubectl apply -f <filename> --namespace=<namespace-name>
# e.g.
kubectl apply -f filename.yaml --namespace=my-namespace
```

## Data And Volumes

- More info can be found in the [docs](https://kubernetes.io/docs/concepts/storage/volumes/).

```text
Volume
------
- A volume in Kubernetes is a directory that can be mounted into a pod.
- Volumes are used to store data that needs to be shared between containers in a pod,
- It's also used to store data that needs to persist even if the pod is restarted.

There are many different types of volumes available in Kubernetes, including:
1.) EmptyDir:
- An emptyDir volume is created when a pod is assigned to a node.
- The data in an emptyDir volume is ephemeral, meaning that it is deleted when the pod is deleted.

2.) HostPath: A hostPath volume mounts a directory or file from the host node's filesystem into your pod.
- A HostPath volume in Kubernetes is a type of volume that mounts a file or directory from the host node's filesystem into a pod.
- This means that the data in the HostPath volume is stored on the host node, and not on a separate storage system.
- HostPath volumes are not as reliable as other types of volumes, such as PersistentVolumes, because they are not backed by a separate storage system. If the host node fails, the data in the HostPath volume will be lost.

3.) ConfigMap:
- A ConfigMap is a way to store configuration data in Kubernetes.
- ConfigMaps can be mounted into pods as volumes, or they can be used to set environment variables in pods.

4.) PersistentVolume:
- A PersistentVolume is a piece of storage that is provisioned by an administrator or dynamically provisioned using Storage Classes.
- PersistentVolumes are used to store data that needs to persist even if the pod is restarted.
```

### EmptyDir

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: my-image
        volumeMounts:
        - name: my-volume
          mountPath: /data
      volumes:
      - name: my-volume
        emptyDir: {}

```

### HostPath

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: my-image:latest
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        hostPath:
          path: /path/on/host
          type: Directory # or DirectoryOrCreate


kubectl get pod second-app-6494c68f48-wbnzb -n defaul -o yaml | kubectl replace --force -f -
```

## Networking

```text
Pod internal
Pod to pod connection
```

### Pod Internal Communication

```text
- Pod internal networking in K8s is a way for containers within the same pod to communicate with each other.
- This means that containers within the same pod can all reach each other's ports using `localhost`.
- An example is shown below where the HOST_NAME == "localhost"

Note
----
- You can also manually copy the IP address of the container
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: second-app
  namespace: development
spec:
  ...

    spec:
      containers:
        - name: app-1
          image: chineidu/other_service:v2
          imagePullPolicy: IfNotPresent # default
          ports:
            - containerPort: 6060
          env:
            - name: HOST_NAME
              value: localhost
```

#### Multiple Containers In One Pods

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: second-app
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-with-db
  template:
    metadata:
      labels:
        app: app-with-db

    spec:
      containers:
        - name: app-1 # container 1
          image: chineidu/other_service:v2
          imagePullPolicy: IfNotPresent # default
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
          ports:
            - containerPort: 6060
          env:
            - name: USERNAME
              valueFrom:
                secretKeyRef:
                  name: my-secret # from secrets.metadata.mane
                  key: username
            - name: PASSWORD
              valueFrom:
                secretKeyRef:
                  name: my-secret
                  key: password
            - name: HOST_NAME
              valueFrom:
                secretKeyRef:
                  name: my-secret
                  key: hostname # localhost

        - name: mongo # container 2
          image: mongo:7.0-rc
          imagePullPolicy: IfNotPresent # default
          resources:
            limits:
              memory: "256Mi"
              cpu: "250m"
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: mongo-volume
              mountPath: /data/db
          env:
            - name: MONGO_INITDB_ROOT_USERNAME
              valueFrom:
                secretKeyRef:
                  name: my-secret
                  key: mongo_initdb_root_username
            - name: MONGO_INITDB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: my-secret
                  key: mongo_initdb_root_password

      volumes:
        - name: mongo-volume
          hostPath:
            path: /data
            type: DirectoryOrCreate
```

### Pod to pod connection

```text
- This involves the communication between two or more pods in K8s node.
- To enable communication, the pods MUST be connected.
- Ways of connecting the pods include:
1. Manually copying the cluster ip of the pod. i.e. if pod 1 want to connect to pod 2, the IP address of pod 1 must be known/copied.
2. Using K8s auto generated environment variables.
3. Using DNS for pod-pod communication.
```

#### 1. Manually Copying The Cluster IP of The Pod

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: second-app
  namespace: development
spec:
  ...

    spec:
      containers:
        - name: app-1
          image: chineidu/other_service:v2
          imagePullPolicy: IfNotPresent # default
          ports:
            - containerPort: 6060
          env:
            - name: HOST_NAME
              value: 10.100.147.172 # pod IP
```

```bash
# To get the pod/cluster IP
kubectl get service -n <namespace>
```

#### 2. Auto Generated Environment Variables

```text
- In Kubernetes, several environment variables are automatically generated and injected into containers by the Kubernetes system.
- These environment variables provide useful information about the running environment and the associated resources.
- Here are some commonly used auto-generated environment variables in Kubernetes:
  POD_NAME: The name of the pod in which the container is running.
  POD_NAMESPACE: The namespace of the pod.
  POD_IP: The IP address assigned to the pod.
  NODE_NAME: The name of the node where the pod is scheduled.
  SERVICE_NAME: The name of the Kubernetes service associated with the pod.
  SERVICE_PORT: The port number of the Kubernetes service associated with the pod.
  HOSTNAME: The hostname of the node where the pod is running.
  KUBERNETES_PORT: The port number of the Kubernetes API server.
  KUBERNETES_SERVICE_HOST: The hostname or IP address of the Kubernetes API server.
  KUBERNETES_SERVICE_PORT: The port number of the Kubernetes API server.
```

```python
# K8s auto generated env vars
import os

# if the name of the service is `mongo-service` (in capital letters),
# then the hostname is f"{name_of_service}_SERVICE_HOST" i.e MONG0_SERVICE_SERVICE_HOST
# e.g
HOST_NAME = os.getenv("MONGO_SERVICE_SERVICE_HOST)

# Note:
"I tried implementing this but I could'nt get it to work 😔"
```

#### 3. DNS For Pod-Pod Communication

```text
- In K8s, DNS (Domain Name System) plays a crucial role in enabling pod-to-pod communication.
- Kubernetes provides an in-cluster DNS service that allows pods to discover and communicate with each other using domain names.
- DNS naming convention for the hostname: <service-name>.<namespace>.
  e.g. if the name of the service is `service-1`, then the hostname is: 'service-1.default'.

Note
----
The default namespace in K8s is `default`.

```

### To Do

```text
1. Data and volumes
2. Networking
3. Ingress
```

## Miscellaneous Commands

```sh
kubectl apply -f k8s_notes/app_1_deployment.yaml -f k8s_notes/app_1_service.yaml
kubectl apply -f k8s_notes/mongo_deployment.yaml -f k8s_notes/mongo_service.yaml
```

## K8s Context

### Get Available Contexts

```sh
kubectl config get-contexts
```

### Get Switch Contexts

```sh
kubectl config use-context <context-name>

# e.g
kubectl config use-context my_local_context
```

### Verify Current Contexts

```sh
kubectl config current-context
```
