# Kubernetes Tutorial

## Table of Content

- [Kubernetes Tutorial](#kubernetes-tutorial)
  - [Table of Content](#table-of-content)
  - [Kubernetes Introduction](#kubernetes-introduction)
  - [K8s Concepts And Architecture](#k8s-concepts-and-architecture)
  - [Installation of Kubernetes \[Locally\]](#installation-of-kubernetes-locally)
    - [Install Kubectl](#install-kubectl)
    - [Install Minikube](#install-minikube)

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

# For more commands
minikube --help
```
