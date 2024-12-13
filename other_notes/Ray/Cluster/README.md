# Ray Cluster

## Table of Content

- [Ray Cluster](#ray-cluster)
  - [Table of Content](#table-of-content)
  - [KubeRay](#kuberay)
  - [RayCluster Quickstart](#raycluster-quickstart)
    - [Run An application On A RayCluster](#run-an-application-on-a-raycluster)
      - [Method 1: Execute a Ray job in the head Pod](#method-1-execute-a-ray-job-in-the-head-pod)
      - [Method 2: Submit a Ray job to the RayCluster Via Ray Job Submission SDK](#method-2-submit-a-ray-job-to-the-raycluster-via-ray-job-submission-sdk)
    - [Access the Ray Dashboard](#access-the-ray-dashboard)
  - [Cleanup](#cleanup)

## [KubeRay](https://github.com/ray-project/kuberay/tree/5b1a5a11f5df76db2d66ed332ff0802dc3bbff76?tab=readme-ov-file#kuberay)

- KubeRay is a powerful, open-source Kubernetes operator that simplifies the `deployment` and `management` of Ray applications on Kubernetes.

- It offers several key components:
  - KubeRay core: This is the official, fully-maintained component of KubeRay that provides three custom resource definitions, RayCluster, RayJob, and RayService. These resources are designed to help you run a wide range of workloads with ease.
    - RayCluster: KubeRay fully manages the lifecycle of RayCluster, including cluster creation/deletion, autoscaling, and ensuring fault tolerance.

    - RayJob: With RayJob, KubeRay automatically creates a RayCluster and submits a job when the cluster is ready. You can also configure RayJob to automatically delete the RayCluster once the job finishes.

    - RayService: RayService is made up of two parts: a RayCluster and a Ray Serve deployment graph. RayService offers zero-downtime upgrades for RayCluster and high availability.

## [RayCluster Quickstart](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#raycluster-quickstart)

- Create a kubernetes cluster using `kind` or `minikube`

```sh
# If you already have a Kubernetes cluster, you can skip this step.
kind create cluster --image=kindest/node:v1.26.0
```

- Deploy the KubeRay operator with the Helm chart repository.

```sh
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update

# Install both CRDs and KubeRay operator v1.2.2.
helm install kuberay-operator kuberay/kuberay-operator --version 1.2.2

# Confirm that the operator is running in the namespace `default`.
kubectl get pods
# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-7fbdbf8c89-pt8bk   1/1     Running   0          27s
```

- Deploy a RayCluster custom resource.
  - Once the KubeRay operator is running, we are ready to deploy a RayCluster. To do so, we create a RayCluster Custom Resource (CR) in the default namespace.

```sh
# Deploy a sample RayCluster CR from the KubeRay Helm chart repo:
helm install raycluster kuberay/ray-cluster --version 1.2.2

# Once the RayCluster CR has been created, you can view it by running:
kubectl get rayclusters

# NAME                 DESIRED WORKERS   AVAILABLE WORKERS   CPUS   MEMORY   GPUS   STATUS   AGE
# raycluster-kuberay   1                 1                   2      3G       0      ready    95s
```

- The KubeRay operator will detect the RayCluster object and will then start your Ray cluster by creating head and worker pods.
- To view Ray cluster’s pods, run the following command:

```sh
# View the pods in the RayCluster named "raycluster-kuberay"
kubectl get pods --selector=ray.io/cluster=raycluster-kuberay

# NAME                                          READY   STATUS    RESTARTS   AGE
# raycluster-kuberay-head-vkj4n                 1/1     Running   0          XXs
# raycluster-kuberay-worker-workergroup-xvfkr   1/1     Running   0          XXs
```

- Wait a few minutes for pods to reach the Running state (mainly for image downloads). Check pending pods with:

```sh
kubectl describe pod raycluster-kuberay-xxxx-xxxxx
```

### Run An application On A RayCluster

#### Method 1: [Execute a Ray job in the head Pod](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#step-4-run-an-application-on-a-raycluster)

- The most straightforward way to experiment with your RayCluster is to exec directly into the head pod. First, identify your RayCluster’s head pod.

```sh
export HEAD_POD=$(kubectl get pods --selector=ray.io/node-type=head -o custom-columns=POD:metadata.name --no-headers)
echo $HEAD_POD
# raycluster-kuberay-head-vkj4n

# Print the cluster resources.
kubectl exec -it $HEAD_POD -- python -c "import ray; ray.init(); print(ray.cluster_resources())"

# 2023-04-07 10:57:46,472 INFO worker.py:1243 -- Using address 127.0.0.1:6379 set in the environment variable RAY_ADDRESS
# 2023-04-07 10:57:46,472 INFO worker.py:1364 -- Connecting to existing Ray cluster at address: 10.244.0.6:6379...
# 2023-04-07 10:57:46,482 INFO worker.py:1550 -- Connected to Ray cluster. View the dashboard at http://10.244.0.6:8265
# {'object_store_memory': 802572287.0, 'memory': 3000000000.0, 'node:10.244.0.6': 1.0, 'CPU': 2.0, 'node:10.244.0.7': 1.0}
```

#### Method 2: [Submit a Ray job to the RayCluster Via Ray Job Submission SDK](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#method-2-submit-a-ray-job-to-the-raycluster-via-ray-job-submission-sdk)

- This method uses the Ray job submission SDK and Ray Dashboard port (8265) to submit jobs to the RayCluster via a Kubernetes service, without requiring commands in the Ray head pod.

```sh
kubectl get service raycluster-kuberay-head-svc

# NAME                          TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                                         AGE
# raycluster-kuberay-head-svc   ClusterIP   10.96.93.74   <none>        8265/TCP,8080/TCP,8000/TCP,10001/TCP,6379/TCP   15m

# Execute this in a separate shell.
kubectl port-forward service/raycluster-kuberay-head-svc 8265:8265

# The following job's logs will show the Ray cluster's total resource capacity, including 2 CPUs.
ray job submit --address http://localhost:8265 -- python -c "import ray; ray.init(); print(ray.cluster_resources())"
```

### Access the Ray Dashboard

- Visit `${YOUR_IP}:8265`in your browser for the Dashboard. For example, http://127.0.0.1:8265.

```sh
export YOUR_IP=127.0.0.1
${YOUR_IP}:8265
```

- See the job you submitted in Step 4 in the Recent jobs pane as shown below.
[![image.png](https://i.postimg.cc/J06pbfYm/image.png)](https://postimg.cc/sGWPzNR0)

## [Cleanup](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#step-6-cleanup)

```sh
# [Step 6.1]: Delete the RayCluster CR
# Uninstall the RayCluster Helm chart
helm uninstall raycluster
# release "raycluster" uninstalled

# Note that it may take several seconds for the Ray pods to be fully terminated.
# Confirm that the RayCluster's pods are gone by running
kubectl get pods

# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-7fbdbf8c89-pt8bk   1/1     Running   0          XXm

# [Step 6.2]: Delete the KubeRay operator
# Uninstall the KubeRay operator Helm chart
helm uninstall kuberay-operator
# release "kuberay-operator" uninstalled

# Confirm that the KubeRay operator pod is gone by running
kubectl get pods
# No resources found in default namespace.

# [Step 6.3]: Delete the Kubernetes cluster
kind delete cluster
```
