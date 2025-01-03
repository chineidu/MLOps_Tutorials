# Docker Tutorial

## Table of Content

- [Docker Tutorial](#docker-tutorial)
  - [Table of Content](#table-of-content)
  - [Introduction](#introduction)
    - [Docker Image](#docker-image)
    - [Docker Container](#docker-container)
    - [Dockerfile](#dockerfile)
    - [Dockerfile Best Practices](#dockerfile-best-practices)
  - [Build A Docker Image And Run A Container](#build-a-docker-image-and-run-a-container)
    - [Build A Docker Image](#build-a-docker-image)
    - [Create And Run A Docker Container](#create-and-run-a-docker-container)
    - [Starting And Stoping Docker Containers](#starting-and-stoping-docker-containers)
  - [Remove Docker Images and Containers](#remove-docker-images-and-containers)
    - [Remove Docker Images](#remove-docker-images)
    - [Remove Containers](#remove-containers)
  - [Inspecting Docker Images And Containers](#inspecting-docker-images-and-containers)
    - [Inspecting Docker Images](#inspecting-docker-images)
    - [Inspecting Docker Containers](#inspecting-docker-containers)
    - [Check Logs](#check-logs)
    - [Exec Into A Docker Container](#exec-into-a-docker-container)
  - [Rename And Push|Pull A Docker Image To|From DockerHub](#rename-and-pushpull-a-docker-image-tofrom-dockerhub)
    - [Login To DockerHub](#login-to-dockerhub)
    - [Rename An Image](#rename-an-image)
    - [Push A Docker Image To DockerHub](#push-a-docker-image-to-dockerhub)
    - [Pull A Docker Image From DockerHub](#pull-a-docker-image-from-dockerhub)
  - [Managing Data](#managing-data)
    - [Types of Data](#types-of-data)
    - [Volumes](#volumes)
      - [Anonymous Volume](#anonymous-volume)
      - [Named Volume](#named-volume)
    - [Bind Mount](#bind-mount)
    - [Read-only Bind Mount](#read-only-bind-mount)
    - [Manage Docker Volumes](#manage-docker-volumes)
    - [Docker Ignore](#docker-ignore)
  - [ARG And ENV Variables](#arg-and-env-variables)
    - [ARG Variables](#arg-variables)
      - [Set ARG Variables Using Dockerfile](#set-arg-variables-using-dockerfile)
      - [Build The Image Using The ARG Variable(s)](#build-the-image-using-the-arg-variables)
    - [ENV Variables](#env-variables)
      - [Set ENV Variables Using Dockerfile](#set-env-variables-using-dockerfile)
      - [Set ENV Variables Using CLI](#set-env-variables-using-cli)
      - [Set ENV Variables Using An ENV File And CLI](#set-env-variables-using-an-env-file-and-cli)
  - [Networking In Docker](#networking-in-docker)
    - [Types of Connections In A Docker Container](#types-of-connections-in-a-docker-container)
      - [1. Connection Between The Docker Container And The Internet (Web)](#1-connection-between-the-docker-container-and-the-internet-web)
      - [2. Connection Between The Docker Container And The Localhost](#2-connection-between-the-docker-container-and-the-localhost)
      - [3. Connection Between The Docker Container And Another Docker Container](#3-connection-between-the-docker-container-and-another-docker-container)
    - [Inter-Process Communication (IPC)](#inter-process-communication-ipc)
  - [Docker Compose](#docker-compose)
    - [Sample Docker-compose File](#sample-docker-compose-file)
    - [Start And Stop The Containers](#start-and-stop-the-containers)
    - [Access Environment Variables In Docker Compose](#access-environment-variables-in-docker-compose)
    - [NOTE](#note)
  - [Deploying Containers](#deploying-containers)
    - [Using EC2 Instances](#using-ec2-instances)
      - [1. Build And Run The Dockerfile On Remote Server (EC2 Instance)](#1-build-and-run-the-dockerfile-on-remote-server-ec2-instance)
      - [2. Build Locally And Run The Dockerfile On Remote Server (EC2 Instance)](#2-build-locally-and-run-the-dockerfile-on-remote-server-ec2-instance)
    - [Using Container Orchestrators](#using-container-orchestrators)
      - [Using Elastic Container Service (ECS)](#using-elastic-container-service-ecs)
        - [1. Using EC2 Launch Type](#1-using-ec2-launch-type)
        - [2. Using Fargate Launch Type](#2-using-fargate-launch-type)
      - [AWS ECR](#aws-ecr)
      - [Update The Deployed Application On ECS Using CLI](#update-the-deployed-application-on-ecs-using-cli)
  - [Debugging](#debugging)

## Introduction

### Docker Image

```text
- Read-only template that defines the contents of a Dockerfile.
- Contains everything needed to run an application including the source code, libraries and config files.
- Images are built using Dockerfiles. i.e. using the docker `build` command.
```

### Docker Container

```text
- Runnable instance of a docker image.
- Created using the docker `run` command.
- Containers share the same underlying operating system kernel but are isolated from each other.
- Docker containers can be run on any machine that has Docker installed.
```

### Dockerfile

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
# Base image
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

### Dockerfile Best Practices

1. **Use a `.dockerignore` File**: Similar to a .gitignore file, a .dockerignore file allows you to exclude unnecessary files and directories from the Docker build context, reducing the build context size.

2. **Base Images**: Use official, well-maintained base images for a smaller footprint and security.

3. **Minimize RUN Instructions and Layer Counts**: Try to chain multiple RUN commands together using `&&` to reduce the number of layers in the final image. This can improve build times and reduce image size.

4. **Order Dockerfile Instructions Strategically**: Place the most frequently changing instructions (e.g., COPY, ADD) towards the end of the Dockerfile, so that the build cache can be leveraged more effectively. i.e. leverage caching.

5. **Avoid Installing Unnecessary Packages**: Only install the packages and dependencies that are required for your application to run. Use a requirements file (e.g., requirements.txt for Python) to manage dependencies.

6. **Combine `RUN` Commands**: Streamline builds by combining related RUN commands with &&.
   - Avoid unnecessary `COPY` or `ADD` instructions, as each one creates a new layer.

7. **Clean Up After Each Step**: Remove any unnecessary files or artifacts after each step to minimize the size of the intermediate layers and reduce the final image size. Use the RUN instruction with && to combine commands and clean up in the same layer.

8. **Parameterize Your Dockerfile**: Use `ARG` and `ENV` instructions to define build-time variables that can be passed during the docker build command. This allows you to easily customize the Dockerfile for different environments or use cases.

9. **Documentation**: Add comments to improve readability and maintainability.

10. **Consistent Naming Convention**: Use a consistent naming convention for your Dockerfiles, such as `Dockerfile.app` or `Dockerfile.db`

## Build A Docker Image And Run A Container

### Build A Docker Image

```shell
docker build -t image_name:tag -f Dockerfile .

# e.g.
docker build -t mlops:v1 -f Dockerfile .

# For more commands
docker build --help
```

### Create And Run A Docker Container

```shell
# Run the container in and interactive mode and publish the exposed ports
docker run -it -p xxxx:xxxx image_name:tag

# e.g.
docker run -it  -p 8000:8000 mlops:v1

# Run the container in a detached `-d` and interactive mode `-it` and publish
# the exposed ports `-p`. Assign a name `--name` to the container and delete the
# container once it's been stopped using the flag`--rm`.
docker run -it -p xxxx:xxxx -d --rm --name container_name image_name:tag

# e.g.
docker run -it -p 8000:8000 -d --rm --name cool_app mlops:v1
# For more commands
docker run --help
```

### Starting And Stoping Docker Containers

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

## Remove Docker Images and Containers

### Remove Docker Images

```shell
# Remove image(s)
docker rmi [image_name|image_id image_name2|image_id image_name3|image_id]
docker image rm [image_name|image_id image_name2|image_id image_name3|image_id]

# e.g.
docker image rm 5a7c0da524ef

# For more commands
docker image --help
```

### Remove Containers

```shell
docker rm [container_name|container_id]

# e.g.
docker rm [5a7c0da524ef|cool_app]

# Remove all stopped containers
docker container prune [container_name|container_id]

# e.g.
docker container prune [5a7c0da524ef|cool_app]
```

## Inspecting Docker Images And Containers

### Inspecting Docker Images

```shell
# Inspect image
docker inspect [image_name|image_id]

# e.g.
docker inspect mlops:v1
```

### Inspecting Docker Containers

```shell
# Inspect container
docker inspect [container_name|container_id]

# e.g.
docker inspect [cool_app|5a7c0da524ef]
```

### Check Logs

```shell
docker logs [container_id|container_name]

# e.g.
docker logs 5a7c0da524ef
```

### Exec Into A Docker Container

```sh
docker exec [options] container_id command [arguments]

# e.g.
docker exec -it 28e04db53aaa sh
```

## Rename And Push|Pull A Docker Image To|From DockerHub

### Login To DockerHub

```shell
docker login

# For more commands
docker login --help
```

### Rename An Image

```shell
# Note: The image has to exist locally!
# You can rename an image using docker `tag` command.
# This command creates a clone/copy of the image.
docker tag old_image_name:tag new_image_name:tag

# e.g.
docker tag mlops:v1 chineidu/mlops:v1
```

### Push A Docker Image To DockerHub

```shell
# Push image to docker hub
docker push account_name/image_name

# e.g.
docker push chineidu/mlops:v1
```

### Pull A Docker Image From DockerHub

```shell
# Pull image to docker hub
docker pull account_name/image_name

# e.g.
docker pull chineidu/mlops:v1
```

## Managing Data

### Types of Data

```text
- Application data
------------------
  - This is the data added to the image and container in the build phase.
  - It contains the code and the environment.
  - It's read-only and can't be changed once the image has been built.

- Temporary App data
--------------------
  - This is the data produced in the running container.
  - It's stored in memory or temporary files.
  - It's read + write + temporary and it's stored in the container.

- Permanent App data
--------------------
  - This is the data produced in the running container.
  - It's stored in files or in a database.
  - It must NOT be lost.
  - It's read + write + permanent and it's stored with `containers` and `volumes`.
```

### Volumes

```text
- A Docker volume is a directory that is mounted into a container.
- Volumes are used to store data that needs to persist outside of the container. e.g. a volume can be used to store configuration files, logs, or data that is generated by the container.


Types of Volumes
----------------

Named volumes
-------------
- They're persistent and can be shared between containers.
- Editing files in the volume is not possible because we don't know exactly where the files are stored.
- Bind mount can be used instead to map a directory to the docker container.

Anonymous volumes
-----------------
- They're temporary and are not shared between containers.
- i.e. data persists if a container is stopped and resumed, but it is lost if the container is destroyed.
```

#### Anonymous Volume

```Dockerfile
# Base image
FROM python:3.10-slim-buster

# Add the image layers
# ...

EXPOSE 8000

# Anonymous volume
VOLUME ["/opt/data"]

# Entry point
CMD [ "python3", "src/main.py", "--host", "0.0.0.0"]
```

```shell
# Another way of adding Anonymous volume
docker -v /docker_dir_name

# e.g.
docker -v /opt/data
```

#### Named Volume

```text
-v local_dir_name:/dir_name_on_docker_container
```

```shell
# Named Volume
docker run -it -p xxxx:xxxx --rm -v local_dir_name:/docker_dir_name image_name:tag

# e.g.
docker run -it -p 8000:8000 --rm -v data:/opt/data mlops:v1
```

### Bind Mount

```text
- A bind mount is a type of mount that allows you to share a directory from your host machine with a container.
- When you use a bind mount, any changes made to the directory on the host machine will be reflected in the container, and vice versa.
- It's set using the terminal and it requires the absolute file/directory path.
```

```shell
# Bind mount
docker -v ${PWD}/local_dir_name:/docker_dir_name

# e.g.
docker run -it -p 8000:8000 --rm \
  -v ${PWD}/data:/opt/data --name cool_app mlops:v1
```

### Read-only Bind Mount

```text
- This means that the container can read but can NOT write data to the volume.
- This is done by adding the suffix `:ro`.
- By default, bind mounts are `read-write`.
```

```shell
# Bind mount [read-only]
docker -v ${PWD}/local_dir_name:/docker_dir_name:ro

# e.g.
docker run -it -p 8000:8000 --rm \
  -v ${PWD}/data:/opt/data:ro --name cool_app mlops:v1
```

### Manage Docker Volumes

```shell
# List all the volumes [bind mounts]
docker volume ls

# Inspect the volumes [bind mounts]
docker volume inspect volume_name

# e.g.
docker volume inspect data


# Remove one or more volumes
docker rm [volume_name1|volume_name2]

# Inspect the volumes [bind mounts]
docker rm data

# For more commands
docker volume --help
```

### Docker Ignore

```text
- A `.dockerignore` file is a text file used by Docker to specify which files and directories should be excluded from the Docker build context when building a Docker image.
- `.dockerignore` file works similarly to a `.gitignore` file used by Git. It allows you to specify patterns of files or directories that Docker should ignore when building the image.
```

- An example of a  `.dockerignore` file can be found [here](https://github.com/chineidu/MLOps_Tutorials/blob/main/.dockerignore).

## ARG And ENV Variables

### ARG Variables

```text
- Scope: ARG variables are only available during the `build` phase of the Docker image.

- Usage: ARG variables are primarily used to pass values to the Dockerfile at build time and can be used in the Dockerfile's instructions, like RUN, ENV, COPY, etc.

- Default values: ARG variables can have default values specified in the Dockerfile using the ARG instruction. These default values can be overridden during the build using the `--build-arg` flag with the docker build command.
```

#### Set ARG Variables Using Dockerfile

```text
- It can only be used during the build phase and NOT run time phase.
- This means that it can not be used with the CMD command in the Dockerfile since it's a container runtime command.
- The default ARG can be overridden using `--build-arg` flag.
- An example is shown below.
```

```dockerfile
# Base image
FROM python:3.10-slim-buster

# Add the image layers
# ...

# Set arg variable(s)
ARG DEFAULT_PORT=8000

# Set env variable(s)
# with a default value of DEFAULT_PORT
ENV PORT ${DEFAULT_PORT}

EXPOSE ${PORT}

# Entry point
CMD [ "python3", "src/fast_api/main.py", "--host", "0.0.0.0"]
```

#### Build The Image Using The ARG Variable(s)

```shell
# Use the default port of 8000 from the Dockerfile
docker build -t mlops:v1 -f Dockerfile .

# Override the default port
docker build -t mlops:v1 --build-arg DEFAULT_PORT=5500 -f Dockerfile .
```

### ENV Variables

```text
- Scope: ENV variables are available both during the `build` phase and when the container is `running`.

-Usage: ENV variables are typically used to set environment variables that can be accessed by processes running inside the container.

- Setting values: ENV variables can be set directly in the Dockerfile using the ENV instruction, or they can be passed as arguments to the docker run command using the -e or --env flag.

- Modifying values: ENV variables can be modified inside the container by using the ENV instruction in a subsequent Dockerfile instruction.
```

#### Set ENV Variables Using Dockerfile

```dockerfile
# Base image
FROM python:3.10-slim-buster

# Add the image layers
# ...

# Set env variables
# with a default value of 8000
ENV PORT 8000

EXPOSE ${PORT}

# Entry point
CMD [ "python3", "src/fast_api/main.py", "--host", "0.0.0.0"]
```

#### Set ENV Variables Using CLI

```text
- You can add ENV variables using the `-e` or `--env` flags.
- You can add as many ENV variables as you want using the flags.
- An example is shown below.
```

```shell
# Use a port of 5000 instead of the default value
docker run -it -p 8000:5000 --env PORT=5000 --rm \
  --name cool_app mlops:v1
```

#### Set ENV Variables Using An ENV File And CLI

```text
- You can add ENV variables using a file. (it's usually called a `.env` file).
- To access the ENV variables in the ENV file, use the `--env-file` flag with the ENV file name.
- An example is shown below.
```

```shell
# Use a port of 5000 instead of the default value
docker run -it -p 8000:5000 --env-file ./.env --rm \
  --name cool_app mlops:v1
```

## Networking In Docker

### Types of Connections In A Docker Container

```text
1. Connection between the docker container and the internet (web).
2. Connection between the docker container and the localhost (local machine).
3. Connection between the docker container and another docker container.
```

#### 1. Connection Between The Docker Container And The Internet (Web)

```text
- This is the default behaviour.
- In order to allow access to the container, the ports must be correctly exposed.
```

#### 2. Connection Between The Docker Container And The Localhost

```text
- You can communicate with a server running on your local machine by using `host.docker.internal`
- e.g. url = "http://host.docker.internal:8000/users"
```

#### 3. Connection Between The Docker Container And Another Docker Container

```text
Method 1 (IP Address):
--------
- To get ip address of a docker container, run `docker container inspect container_name`
- Update the address of the url you want to connect with using the ip address of the container.
- e.g. url = "http://172.17.0.2:8000/users"


Method 2 (Using Network):
--------
- Create a network that all the containers can communicate with using the command: `docker network create network_name`
- Connect to the created network by using the flag `--network network_name`
- Once the network has been created and connected to, update the url using the container's name.
- e.g. url = "http://container_name:8000/users"

NOTE:
----
- Communication between containers requires all containers to be connected to the `SAME` Docker network.
```

```shell
# Create docker network
docker network create network_name

# e.g.
docker network create api_network

# View all existing networks
docker network ls

# Connect to a docker network
# The network's name is: api_network
# image: mlops:v1
docker run -it -p 8000:8000 --name cool_app --rm --network api_network mlops:v1

# For more commands
docker network --help
```

### Inter-Process Communication (IPC)

- In a Docker Compose file, the `ipc: host` configuration specifies that the container will share the host machine's Inter-Process Communication (IPC) namespace.
- This means the container can access and utilize the same IPC resources (e.g., shared memory, semaphores, message queues) as the processes running directly on the host system.
- Breakdown:
  - **IPC Namespace**: An IPC namespace acts as a separation mechanism for processes. Processes within the same namespace can communicate with each other using IPC mechanisms, while processes in different namespaces are isolated.
  - **Shared Resources**: When you set ipc: host, the container essentially joins the host's IPC namespace, granting it access to shared memory segments, semaphores, and message queues already established on the host machine.

## Docker Compose

```text
- Docker Compose is a tool that helps you define and run multi-container applications.
- With Compose, you can create a YAML file that defines the services that make up your application. Then, with a single command, you can start up all of the services in your application.
- You can add a custom network but by default, docker-compose create a network for all the containers to communicate with one another.

Docs:
-----
https://docs.docker.com/compose/compose-file/compose-file-v3/
```

- An example docker-compose file can be found [here](https://github.com/chineidu/MLOps_Tutorials/blob/main/docker-compose.yml)

### Sample Docker-compose File

```yml
version: "3.8"

services:
  my_app:
    build:
      context: ./other
      dockerfile: Dockerfile
    image: other_service:v1
    container_name: other_app
    environment:
      - OTHER_URL=http://cool_app:8000/users
      - USERNAME=neidu
      - PASSWORD=password

    # OR (Another way of passing env vars)
    # Location of file(s) containing the env vars. Only accessed by the container.
    env_file:
      - abs_path/to/env_file # e.g. folder/env_file

    ports:
      - 6060:6060
    volumes:
      - ./other:/opt # Bind mount
    depends_on:
      - mongodb
```

### Start And Stop The Containers

```shell
# Start ALL Containers
docker-compose up

# Start Specific Containers
docker-compose up -d service_1 service_2

# Start Containers (Force build)
docker-compose up --build

# For more commands
docker-compose up --help

# Stop Containers
docker-compose down
```

### Access Environment Variables In Docker Compose

```sh
docker-compose --env-file ./path/to/env/file command

# e.g.
docker-compose --env-file ./envs/mlflow_dev.env up
```

### NOTE

```text
- Bind mounts (volumes) are only recommended during development.
- For production purposes, you can copy the a snapshop of the required files/folders in the dockerfile during the build phase.
```

## Deploying Containers

```text
There are a few ways of deploying docker containers in cloud provider. e.g. AWS.

1. EC2 Instances: You can also deploy Docker containers directly on EC2 instances. In this approach, you provision EC2 instances, install Docker, and manage the container deployment and scaling manually. This method provides more flexibility but requires more operational overhead compared to the managed services mentioned above.

2. Amazon Elastic Container Service (ECS): ECS is a fully managed container orchestration service provided by AWS. It supports Docker containers and allows you to easily run and scale containerized applications. ECS provides features like auto-scaling, load balancing, and integration with other AWS services.

3. AWS Fargate: Fargate is a serverless compute engine for containers on AWS. It allows you to run containers without managing the underlying infrastructure. Fargate integrates with ECS and EKS, enabling you to deploy Docker containers as tasks or pods, respectively, without worrying about the server infrastructure.

4. Amazon Elastic Kubernetes Service (EKS): EKS is a managed Kubernetes service that simplifies the deployment and management of Kubernetes clusters on AWS. With EKS, you can deploy Docker containers as part of Kubernetes pods and take advantage of Kubernetes features for container orchestration.


Other methods:

5. AWS Lambda: While not specifically designed for Docker containers, AWS Lambda is a serverless compute service that allows you to run code without provisioning or managing servers. You can package your application as a Docker container and deploy it as a Lambda function using the AWS Lambda Container Image Support.

6. AWS Batch: AWS Batch is a fully managed service for running batch computing workloads. It allows you to run Docker containers as part of batch jobs, which can be useful for processing large amounts of data or performing compute-intensive tasks.
```

### Using EC2 Instances

- Docker can be installed on an EC2 instance using [this](https://www.cyberciti.biz/faq/how-to-install-docker-on-amazon-linux-2/).

```shell
# Apply pending updates
sudo yum update

# Install docker, run
sudo yum install docker

# Add group membership for the default ec2-user so you can run
# all docker commands without using the sudo command
sudo usermod -a -G docker ec2-user
id ec2-user

# Reload a Linux user's group assignments to docker w/o logout
newgrp docker

# Start the Docker service
sudo systemctl start docker.service
```

#### 1. Build And Run The Dockerfile On Remote Server (EC2 Instance)

```text
This involves:
- Create EC2 instance(s) and SSH into them.
- Install Docker on the remote server.
- Save the source code and the Dockerfile on the remote server.
- Build and run the Docker container on the remote server.

Note:
-----
- This approach is not advisable.
```

#### 2. Build Locally And Run The Dockerfile On Remote Server (EC2 Instance)

```text
This involves:
- Build the docker image locally and push the built image to a remote Docker repository like Dockerhub.
- Create EC2 instance(s) and SSH into them.
- Install Docker on the remote server.
- Pull the Docker image from the remote Docker repository and run the Docker container on the remote server.

Note:
-----
- This is better than the first method but requires a lot of managing by the developer.
```

### Using Container Orchestrators

```text
Container Orchestrator
----------------------
- A container orchestrator is a software tool that automates the deployment, scaling, and management of containerized applications. Container orchestration is essential for running large-scale containerized applications, as it can help to ensure that applications are running reliably and efficiently.


Features:
---------
- Deployment And Load Balanceing: Container orchestrators can automatically deploy containerized applications to a cluster of hosts. This can be done in a rolling or blue-green deployment, depending on the application's requirements.

- Scaling: Container orchestrators can automatically scale containerized applications up or down based on demand. This can help to ensure that applications are always running at the optimal number of containers.

- Management: Container orchestrators can help to manage containerized applications by providing features such as health monitoring, logging, and tracing. This can help to identify and resolve problems with applications quickly and easily.


Examples of Container Orchestrator
----------------------------------
1. ECS
2. EKS (AWS K8s managed service)
3. K8s (Open source)
4. Docker Swarm
```

#### Using Elastic Container Service (ECS)

```text
Cluster
-------
- This is the physical resources the containers will run on.

Task Definition
---------------
- A task definition is a blueprint that describes how a Docker container should be launched and run within a cluster.
- It defines various parameters such as the container image, CPU and memory requirements, networking settings, logging configuration, and more.

Task
----
- This is an instance of a task definition.

Service
-------
- This ensures that a certain number of `tasks` are running at all times.
- It restarts contains exited/crashed containers.

Load Balancer
-------------
- A load balancer is a device that distributes (routes) network or application traffic across a number of servers.
- Load balancers are used to increase capacity (concurrent users) and reliability of applications.

```

##### 1. Using EC2 Launch Type

```text
- It allows you to run containerized applications on Amazon Elastic Compute Cloud (EC2) instances that you manage yourself.

- When you choose to use the EC2 launch type, you maintain control over your infrastructure but are required to provision, scale, and monitor EC2 instances.


Benefits
--------
- Control: You have full control over your infrastructure, including the type and size of EC2 instances, the operating system, and the networking configuration.

- Flexibility: You can use the EC2 launch type to run a wide variety of containerized applications, including those that require specific hardware or software configurations.

- Cost-effectiveness: You can optimize your costs by using Spot Instances or Reserved Instances.


Drawbacks
---------
- Complexity: Managing EC2 instances can be complex, especially if you need to scale your application.

- Security: You are responsible for securing your EC2 instances and the data that they store.

- Maintenance: You are responsible for maintaining your EC2 instances, including patching and updating the operating system and applications.
```

##### 2. Using Fargate Launch Type

- The tutorial can be found [here](https://www.youtube.com/watch?v=esISkPlnxL0&t=1243s).

```text
- The AWS Fargate launch type is a `serverless` compute engine that lets you run docker containers without provisioning or managing servers.

- With Fargate, you specify your container's resource requirements and Fargate provisions the right amount of compute, memory, and storage for your container.

- Fargate then runs and manages your containers across a fleet of Amazon Elastic Compute Cloud (EC2) instances.


Benefits
--------
- Serverless: Fargate is a serverless compute engine, which means that you do not need to provision or manage servers. This can save you time and money.

- Scalable: Fargate is scalable, which means that you can easily scale your applications up or down based on demand. This can help you to save money by only paying for the resources that you use.

- Managed: Fargate is a managed service, which means that Amazon ECS handles the provisioning, scaling, and management of the underlying infrastructure. This can save you time and effort.

- Secure: Fargate is a secure service, which means that Amazon ECS handles the security of the underlying infrastructure. This can help you to protect your applications and data.


Drawbacks
---------
- Limited flexibility: Fargate is a managed service, which means that you have less flexibility than if you were to provision and manage your own servers.

- Not all workloads are supported: Not all workloads are supported by Fargate. If you have a workload that requires specific hardware or software configurations, you may need to use the ECS EC2 launch type.

- Cost: Fargate can be more expensive than the ECS EC2 launch type for some workloads. This is because you pay for the resources that you use, even when your application is not running.

NOTE
----
- ECS does not support using the service/container name as the IP/hostname.
- `localhost` is used instead.
- e.g.
  - instead of:  url = "http://container_name:8000/users",
  we use:  url = "http://localhost:8000/users"

STEPS:
1. Create a cluster.
2. Create task definition(s).
   - Inorder to add volumes to the task definition, `EFS` is used and it requires a security group with an `NFS` network type.
3. Create a service or task(s).
   - Create a new security group for the service/task (or use an existing security group).
   - Remember to expose the necessary port(s) by adding `inbound rules` to the security group.
   - If a service was created, you can add an `application` load balancer and auto scaling.
```

#### AWS ECR

- [AWS Docs](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)

```shell
# Environment variables
export PROFILE_NAME="yourProfileName"
export AWS_ACCOUNT_ID="yourAccountID"
export AWS_REPOSITORY_NAME="yourAWSRepositoryName"
export IMAGE_NAME="yourIMAGEName"
export TAG="yourTag"
export AWS_REGION="yourAWSRegion"


# Set Default AWS Profile
aws configure --profile=${PROFILE_NAME}


# Authenticate your Docker client to the Amazon ECR registry
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS \
  --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com


# Identify the local image to push. Run the docker images command to list the container images on your system.
docker images

# Tag your image with the Amazon ECR registry
docker tag ${IMAGE_NAME}:${TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_REPOSITORY_NAME}:${TAG}

# Push the image using the docker push command
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_REPOSITORY_NAME}:${TAG}
```

#### Update The Deployed Application On ECS Using CLI

```text
- Once the application has been deployed on ECS (using AWS console), updates made to the source code can be pushed to the deployed cluster using AWS ECS CLI.
```

```shell
export CLUSTER_NAME="yourECSClusterName"
export SERVICE_NAME="yourECSServiceName"
export TASK_DEFINITION_NAME="yourECSTaskDefinitionName"

export CLUSTER_NAME="ProdCluster"
export SERVICE_NAME="ml-service"
export TASK_DEFINITION_NAME="ml-app"

# Update the deployed app
aws ecs update-service --cluster ${CLUSTER_NAME} --service ${SERVICE_NAME} \
  --task-definition  ${TASK_DEFINITION_NAME} --force-new-deployment

# Monitor Deployment Progress
aws ecs describe-services --cluster ${CLUSTER_NAME} --services ${SERVICE_NAME}

```

- Possible [gotchas](https://github.com/aws/containers-roadmap/issues/333)

## Debugging

- Try the following commands:

```sh
# List all containers
docker ps -a
# Stop all containers
docker stop $(docker ps -a -q)
# Remove stopped containers
docker system prune -f

# List all the Docker networks on your system
docker network ls
# Check if anything is bound to $PORT
netstat -tuln | grep $PORT

# Identify PID
sudo lsof -i :$PORT
sudo kill -9 [PID]
```
