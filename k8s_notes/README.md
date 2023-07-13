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
      - [List All The Resources In A K8s Cluster](#list-all-the-resources-in-a-k8s-cluster)
      - [Node Port](#node-port)
      - [Load Balancer](#load-balancer)
    - [Environment Variables](#environment-variables)
    - [Secret Config File](#secret-config-file)
      - [To Do](#to-do)

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
kubectl get logs <pod-name>

# Show the last 5 logs
kubectl logs second-app-6695467d49-bwhgg --tail=5

# Show the logs within the last 10 seconds
kubectl logs second-app-6695467d49-bwhgg --since=10s

# Specify if the logs should be streamed.
kubectl logs second-app-6695467d49-bwhgg --follow=true

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

#### To Do

```text
1. Data and volumes
2. Networking
3. Ingress
```
