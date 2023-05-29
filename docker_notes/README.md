# Docker Notes

## Table of Content

- [Docker Notes](#docker-notes)
  - [Table of Content](#table-of-content)
  - [Docker Image](#docker-image)
  - [Docker Container](#docker-container)
  - [Dockerfile](#dockerfile)
  - [Build A Docker Image](#build-a-docker-image)
  - [Create And Run A Docker Container](#create-and-run-a-docker-container)
  - [Starting And Stoping Docker Containers](#starting-and-stoping-docker-containers)
  - [Remove Docker Images](#remove-docker-images)
  - [Remove Docker Containers](#remove-docker-containers)
  - [Inspecting Docker Images and Containers](#inspecting-docker-images-and-containers)

## Docker Image

```text
- Read-only template that defines the contents of a Dockerfile.
- Contains everything needed to run an application including the source code, libraries and config files.
- Images are built using Dockerfiles. i.e. using the docker `build` command.
```

## Docker Container

```text
- Runnable instance of a docker image.
- Created using the docker `run` command.
- Containers share the same underlying operating system kernel but are isolated from each other.
- Docker containers can be run on any machine that has Docker installed.
```

## Dockerfile

```text
- A Dockerfile is a text file that contains instructions on how to build a Docker image. It is a simple text file that contains a series of instructions that are executed in order to create a Docker image. The instructions in a Dockerfile can be used to install software, copy files, and configure settings.

- Useful commands:
    FROM: This instruction specifies the base image that your image will be built on.
    RUN: This instruction executes a command in the shell.
    COPY: This instruction copies files from your local machine to the image.
    ADD: This instruction is similar to COPY, but it can also download files from the internet.
    ENV: This instruction sets an environment variable in the image.
    CMD: This instruction specifies the command that will be run when the container starts.

- An example is shown below:
```

```Dockerfile
FROM python:3.10-slim-buster

# Create working directory
WORKDIR /opt

# Copy and install dependencies. This should be here to avoid
# re-installing the packages when there's a minor change in the Docker image.
COPY ["./requirements.txt", "./"]
RUN pip install -r requirements.txt

# Copy source code
COPY ["./", "./"]

EXPOSE 8000

# Entry point
CMD [ "python3", "src/main.py", "--host", "0.0.0.0"]

```

## Build A Docker Image

```shell
docker build -t image_name:version -f Dockerfile .

# e.g.
docker build -t mlops:v1 -f Dockerfile .

# For more commands
docker build --help
```

## Create And Run A Docker Container

```shell
# Run the container in and interactive mode and publish the exposed ports
docker run -it image_name:version -p xxxx:xxxx

# e.g.
docker run -it mlops:v1 -p 8000:8000

# Run the container in a detached and  interactive mode and publish
# the exposed ports. Assign a name to the container and delete the
# container once it's been stopped.
docker run -it -d --rm image_name:version --name container_name -p xxxx:xxxx

# e.g.
docker run -it -d --rm mlops:v1 --name cool_app -p 8000:8000

# For more commands
docker run --help
```

## Starting And Stoping Docker Containers

```shell
# List all containers
docker ps -a

# Start a container
docker start container_name
docker start container_id

# Stop a container
docker stop container_name
docker stop container_id

# For more commands
docker [start|stop] --help
```

## Remove Docker Images

```shell
# Remove image(s)
docker rmi image_name image_name2 image_name3
docker image rm image_name image_name2 image_name3
docker image rm image_id image_id2 image_id3

# e.g.
docker image rm 5a7c0da524ef

# For more commands
docker image --help
```

## Remove Docker Containers

```shell
# Remove container(s)
docker rm container_1 container_2 container_3

# e.g.
docker rm 5a7c0da524ef
```

## Inspecting Docker Images and Containers

```shell
# Inspect image
docker image inspect [image_name|image_id]

# e.g.
docker image inspect 5a7c0da524ef

# Inspect container
docker inspect [container_name|image_id]

# e.g.
docker inspect mlops:v1
```
