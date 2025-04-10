# Helm

## Table of Content

- [Helm](#helm)
  - [Table of Content](#table-of-content)

## Installation

- Using homebrew:

```sh
brew install helm
```

## Helm Charts

### Install Helm Chart From Repo

- You can follow the instructions [here](https://artifacthub.io/packages/helm/bitnami/mysql?modal=install)

```sh
# Install App (MySQL) Helm Chart
# THe RELEASE_NAME has to be unique
APP_NAME="mysql"
RELEASE_NAME="my-${APP_NAME}"
REPO_NAME="bitnami"
REPO_URL="https://charts.bitnami.com/bitnami"
VERSION="12.0.1"
NAMESPACE_NAME="default"

# Add the Helm repository
helm repo add ${REPO_NAME} ${REPO_URL}

# Install
helm install ${RELEASE_NAME} ${REPO_NAME}/${APP_NAME} --version ${VERSION} --namespace ${NAMESPACE_NAME}
```

#### Get all the helm releases

```sh
helm ls --all-namespaces

# Show all releases in all namespaces (including deleted ones and their history)
helm ls --all-namespaces -a
```

#### Display the status of the helm release

```sh
helm status <my-release>

# E.g.
helm status $RELEASE_NAME
```

### Uninstall Helm Chart

```sh
# --keep-history will keep the release history and allow you to rollback to previous versions
helm uninstall ${RELEASE_NAME} --namespace ${NAMESPACE_NAME} --keep-history
```

### Get Helm Chart Release History

```sh
helm history $RELEASE_NAME -n $NAMESPACE_NAME
```

## Create An App With Helm Chart

### Steps

#### 1.) Create a new Helm chart

```sh
helm create <chart-name>
# e.g.
helm create rmq-app
```

#### 2.) Update the values.yaml file

```yaml
# values.yaml
---
rabbitmq:
  image: rabbitmq:4.0-management
  containerName: local-rabbitmq
  resources:
    limits:
      cpu: 1
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
  ports:
    - name: amqp
      port: 5672
      targetPort: 5672
    - name: management
      port: 15672
      targetPort: 15672
  storage:
    size: 1Gi
  healthcheck:
    path: "/api/healthcheck"
    initialDelaySeconds: 30
    periodSeconds: 30
    timeoutSeconds: 10
    failureThreshold: 5

worker:
  image: chineidu/rmq-worker:v1
  replicas: 3
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 256Mi

producer:
  image: chineidu/rmq-producer:v1
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 256Mi

```

#### 3.) Update the deployment.yaml file

```yaml
# rabbitmq-deployment.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-rabbitmq
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{ .Release.Name }}-rabbitmq
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}-rabbitmq
    spec:
      containers:
      - name: {{ .Values.rabbitmq.containerName }}
        image: {{ .Values.rabbitmq.image }}
        ports:
        {{- range .Values.rabbitmq.ports }}
        - containerPort: {{ .targetPort }}
          name: {{ .name }}
        {{- end }}
        resources:
          limits:
            cpu: {{ .Values.rabbitmq.resources.limits.cpu }}
            memory: {{ .Values.rabbitmq.resources.limits.memory }}
          requests:
            cpu: {{ .Values.rabbitmq.resources.requests.cpu }}
            memory: {{ .Values.rabbitmq.resources.requests.memory }}
        envFrom:
        - configMapRef:
            name: {{ .Release.Name }}-config
        volumeMounts:
        - name: rabbitmq-data
          mountPath: /var/lib/rabbitmq
        livenessProbe:
          exec:
            command: ["rabbitmq-diagnostics", "check_port_connectivity"]
          initialDelaySeconds: {{ .Values.rabbitmq.healthcheck.initialDelaySeconds }}
          periodSeconds: {{ .Values.rabbitmq.healthcheck.periodSeconds }}
          timeoutSeconds: {{ .Values.rabbitmq.healthcheck.timeoutSeconds }}
          failureThreshold: {{ .Values.rabbitmq.healthcheck.failureThreshold }}
        readinessProbe:
          exec:
            command: ["rabbitmq-diagnostics", "check_port_connectivity"]
          initialDelaySeconds: {{ .Values.rabbitmq.healthcheck.initialDelaySeconds }}
          periodSeconds: {{ .Values.rabbitmq.healthcheck.periodSeconds }}
          timeoutSeconds: {{ .Values.rabbitmq.healthcheck.timeoutSeconds }}
          failureThreshold: {{ .Values.rabbitmq.healthcheck.failureThreshold }}
      volumes:
      - name: rabbitmq-data
        persistentVolumeClaim:
          claimName: {{ .Release.Name }}-rabbitmq-data
```

#### 4.) Update the service.yaml file

```yaml
# rabbitmq-service.yaml
---
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-rabbitmq
spec:
  selector:
    app: {{ .Release.Name }}-rabbitmq
  ports:
  {{- range .Values.rabbitmq.ports }}
    - name: {{ .name }}
      port: {{ .port }}
      targetPort: {{ .targetPort }}
  {{- end }}
```

#### 5.) Add Persistent Volume Claim (

- This is optional if you want to use a Persistent Volume.

```yaml
# rabbitmq-pvc.yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Release.Name }}-rabbitmq-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: {{ .Values.rabbitmq.storage.size }}
```

#### 6.) Add Other Deployments

- Depending on your application, you may need to add other deployments, services, and other resources.

#### 7.) Add the ConfigMap

- This is optional if you want to use a ConfigMap.
- It is used to store the configuration and credentials for your application.

```yaml
# configmap.yaml
---
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
data:
  RABBITMQ_DEFAULT_USER: "guest"
  RABBITMQ_DEFAULT_PASS: "guest"
```

### 8.) Create the Helm Chart

```sh
helm install rmq-app .
```

### 9.) Update the Helm Chart

- You can update the Helm Chart by running the following command:

```sh
helm upgrade rmq-app .
```

### 10.) Check the Helm Chart

- You can check the Helm Chart by running the following command:

```sh
helm ls
# OR
helm list
```

### 11.) Confirm the Deployment/Service

- You can confirm the deployment by running the following command:

```sh
kubectl get pods
kubectl get services
```

### 12.) Delete the Helm Chart

- You can delete the Helm Chart by running the following command:

```sh
helm delete <RELEASE_NAME>
# e.g.
helm delete rmq-app
```
