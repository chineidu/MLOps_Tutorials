# Kubernetes Tutorial

## Table of Content

- [Kubernetes Tutorial](#kubernetes-tutorial)
  - [Table of Content](#table-of-content)
  - [Kubernetes Introduction](#kubernetes-introduction)
  - [K8s Concepts And Architecture](#k8s-concepts-and-architecture)
  - [Installation of Kubernetes \[Locally\]](#installation-of-kubernetes-locally)
    - [Install Kubectl](#install-kubectl)
    - [Install Minikube](#install-minikube)
  - [Objects In K8s](#objects-in-k8s)
    - [Pod Object](#pod-object)
    - [Deployment Object](#deployment-object)
      - [Deployment \[Imperative Approach\]](#deployment-imperative-approach)
      - [Expose A Deployment](#expose-a-deployment)
      - [Scaling Deployments](#scaling-deployments)
      - [Updating Deployments \[With Docker Images\]](#updating-deployments-with-docker-images)

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
kubectl get po -A

# Launch the minikube dashboard
minikube dashboard

# For more commands
minikube --help
```

## Objects In K8s

### Pod Object

```text
- A pod is the smallest and most basic unit of deployment.

- Containers within a pod share the same network namespace, allowing them to communicate with each other over the `localhost` interface. They can also share storage volumes, which are mounted into the containers' file systems.

- Pods are considered to be ephemeral and disposable. If a pod fails or needs to be rescheduled due to node failures or scaling events, a new pod can be created to replace it.

- It's important to note that pods are not intended to be directly exposed to external network traffic. Instead, Kubernetes introduces other higher-level abstractions, such as `services`, to provide stable network endpoints and load balancing for pods.
```

### Deployment Object

```text
- Deployment objects are a way to manage applications declaratively.

- Deployment objects describe the desired state of an application and K8s takes care of the details of how to update the pods that make up the application.

- Deployment objects can be used to scale applications up or down, and they can also be rolled back if an update fails.

Create A K8s Deployment (Imperative Approaach)
-----------------------
1. Build an image and push to a Docker repository like Dockerhub.
2. Start a K8s cluster. e.g. using minikube for local K8s deployment.
3. Create a deployment object using `kubectl`.
4. Expose the pod(s) to the outside world using a K8s `service`.

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

# List all the running pods in your K8s cluster.
kubectl get pods

# List all the created deployments in your K8s cluster.
kubectl get deployments

# Delete a K8s deployment.
kubectl delete deployment <deployment_name>

# Check the status of the deployment using the dashboard
minikube dashboard
```

#### Expose A Deployment

```text
- For the deployment to be accessed by the outside world, it has to be exposed as a `service`.
```

```bash
# Expose a K8s resource, such as a pod, deployment, or replica set, as a service.
# The service will be created in the default namespace, unless a different namespace is specified.
kubectl expose <resource> [options]
# For deployment, it'll look like this
kubectl expose deployment <deployment_name> --type=[ClusterIP|NodePort|LoadBalancer] --port=$PORT
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
