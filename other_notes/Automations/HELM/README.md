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
