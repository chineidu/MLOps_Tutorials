# KIND (Kubernetes IN Docker)

Docs can be found at this [KIND Quick Start Guide](https://kind.sigs.k8s.io/docs/user/quick-start/)

<!-- TOC -->

- [KIND Kubernetes IN Docker](#kind-kubernetes-in-docker)
  - [Overview](#overview)
    - [Installation](#installation)
  - [Create kind cluster](#create-kind-cluster)
    - [Create a cluster with 3 nodes one control-plane and two workers](#create-a-cluster-with-3-nodes-one-control-plane-and-two-workers)
  - [List clusters](#list-clusters)
  - [Delete cluster](#delete-cluster)
  - [Get K8s Current Context](#get-k8s-current-context)
  - [Switch K8s Context](#switch-k8s-context)
  - [Add kubernetes-dashboard repository](#add-kubernetes-dashboard-repository)
  - [Deploy the Kubernetes Dashboard](#deploy-the-kubernetes-dashboard)
  - [Deploy a Helm Chart](#deploy-a-helm-chart)
  - [List helm repositories](#list-helm-repositories)
  - [Delete a Helm release](#delete-a-helm-release)
  - [Access the Kubernetes Dashboard](#access-the-kubernetes-dashboard)
    - [Create a Service Account And ClusterRoleBinding](#create-a-service-account-and-clusterrolebinding)
    - [Create a Bearer Token for the Service Account](#create-a-bearer-token-for-the-service-account)
      - [Create A Long-Lived Token](#create-a-long-lived-token)
    - [Command Line Proxy](#command-line-proxy)
    - [Access the Dashboard](#access-the-dashboard)

<!-- /TOC -->

## Overview

KIND (Kubernetes IN Docker) is a tool for running local Kubernetes clusters using Docker containers as nodes. It is primarily designed for testing Kubernetes itself, but it can also be used for local development and CI/CD pipelines.

### [Installation](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

```sh
# Install KIND using Brew (macOS/Linux)
brew install kind
```

## Create kind cluster

```sh
kind create cluster --name <your-cluster-name>
# E.g

kind create cluster --name single-node-cluster

```

### Create a cluster with 3 nodes (one control-plane and two workers)

```yaml
# three-node-cluster.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

- Create the cluster

```sh
kind create cluster --name <your-cluster-name> --config three-node-cluster.yaml

# E.g
kind create cluster --name three-node-cluster --config three-node-cluster.yaml
```

## List clusters

```sh
kind get clusters
```

## Delete cluster

``` sh
kind delete cluster --name <your-cluster-name>

# E.g

kind delete cluster --name single-node-cluster
```

## Get K8s Current Context

```sh
kubectl config current-context
```

## Switch K8s Context

```sh

kubectl config use-context <your-cluster-name>
```

## Add kubernetes-dashboard repository

```sh
helm repo add kubernetes-dashboard <https://kubernetes.github.io/dashboard/>
```

## Deploy the Kubernetes Dashboard

```sh
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```

## Deploy a Helm Chart

```sh
helm install <release-name> <chart> [flags] --namespace <namespace>

# E.g

helm install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --namespace kubernetes-dashboard
```

## List helm repositories

```sh
helm repo list
```

## Delete a Helm release

```sh
helm uninstall <release-name> --namespace <namespace>
```

## Access the Kubernetes Dashboard

### Create a Service Account And ClusterRoleBinding

- If service account and clusterrolebinding has not been already created.

```yaml
# dashboard-adminuser.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
---
# ClusterRoleBinding to give the Service Account admin privileges
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
```

- Create the Service Account and ClusterRoleBinding

```sh
# Delete if already exists before creating
kubectl delete -f dashboard-adminuser.yaml --ignore-not-found

# Create the Service Account and ClusterRoleBinding
kubectl create -f dashboard-adminuser.yaml
```

### Create a Bearer Token for the Service Account

```sh
kubectl -n <namespace> create token <service-account-name>

# E.g
kubectl -n kubernetes-dashboard create token kubernetes-dashboard
```

#### Create A Long-Lived Token

```yaml
# dashboard-adminuser-long-lived.yaml
apiVersion: v1
kind: Secret
metadata:
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: "kubernetes-dashboard"
type: kubernetes.io/service-account-token
```

- Create the long-lived token

```sh
kubectl get secret kubernetes-dashboard -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 -d
```

### Command Line Proxy

```sh
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

```

### Access the Dashboard

- Open your web browser and navigate to:

  <https://localhost:8443/>

- Use the token created in step 3 to log in to the dashboard

- Note: Use `https` and not `http`
