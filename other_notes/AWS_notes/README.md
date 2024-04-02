# AWS CLI And GOOGLE CLOUD CLI Tutorial

## Table of Content

- [AWS CLI And GOOGLE CLOUD CLI Tutorial](#aws-cli-and-google-cloud-cli-tutorial)
  - [Table of Content](#table-of-content)
  - [AWS Common Operations](#aws-common-operations)
    - [Copy Files](#copy-files)
    - [List Objects In A Bucket](#list-objects-in-a-bucket)
  - [Google Cloud Platform](#google-cloud-platform)
    - [Cheat Sheet](#cheat-sheet)
    - [Set GCP Region and Zone](#set-gcp-region-and-zone)
    - [Upload Files](#upload-files)
    - [Push Docker Images To Artifacts Registry](#push-docker-images-to-artifacts-registry)

## AWS Common Operations

### Copy Files

```sh
aws s3 cp <s3://bucket> <destination/file/path> --recursive

# e.g.
aws s3 cp s3://my-special-bucket/huge_data.parquet/ ./data --recursive
```

### List Objects In A Bucket

```sh
aws s3 ls <s3://bucket>

# e.g.
aws s3 ls s3://my-special-bucket/raw_trans_data/
```

---

## Google Cloud Platform

### Cheat Sheet

```sh
gcloud cheat-sheet
```

### [Set GCP Region and Zone](https://cloud.google.com/compute/docs/gcloud-compute#set_default_zone_and_region_in_your_local_client)

```sh

gcloud config set compute/region eu-west2
gcloud config set compute/zone eu-west2-a
```

### Upload Files

- Uploading a Single File

```sh
gcloud storage cp [local_file_path] [gs://bucket_name/destination_object_name]

# e.g.
gcloud storage cp Makefile gs://neidu_ml_buket/Makefile
```

- Uploading Multiple Files or Directories:
  - Use the `-r` flag to recursively upload entire directories and their contents

```sh
gcloud storage cp -r [local_directory_path] [gs://bucket_name/destination_prefix]

# e.g.
gcloud storage cp -r ./data gs://neidu_ml_buket/data
```

### Push Docker Images To Artifacts Registry

- After creating a docker artifacts registry, on the console, click on `SETUP INSTRUCTIONS` and copy and run the command:

```sh
# Authentication
gcloud auth configure-docker \
    europe-west2-docker.pkg.dev
```

- Tag (rename) your docker image using the format:

```sh
export GCP_DOCKER_ALIAS="europe-west2-docker.pkg.dev"
export PROJECT_ID="ml-awesome-123456"
export DOCKER_REPO_NAME="ml-docker-repo"

docker tag your_image:your_tag \
  ${GCP_DOCKER_ALIAS}/${PROJECT_ID}/${DOCKER_REPO_NAME}/your_image:your_tag

# e.g.
docker tag qdrant/qdrant:latest \
  ${GCP_DOCKER_ALIAS}/${PROJECT_ID}/${DOCKER_REPO_NAME}/qdrant:v2
```

- Push Docker image to Google Artifacts Registry

```sh
docker push ${GCP_DOCKER_ALIAS}/${PROJECT_ID}/${DOCKER_REPO_NAME}/qdrant:v2
```
