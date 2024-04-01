# MLOps_Tutorials

This course contains tutorials for Docker, K8s, Model deployment, ML Systems Testing and Monitoring, etc.

This repo was inspired by the following Udemy courses:

1. **Docker**: [Docker notes](https://github.com/chineidu/MLOps_Tutorials/tree/main/docker_notes)
   - Course: [Docker and k8s](https://www.udemy.com/course/docker-kubernetes-the-practical-guide/learn/practice/1244330/summary#overview)
2. **Kubernetes**: [K8s notes](https://github.com/chineidu/MLOps_Tutorials/tree/main/k8s_notes)
   - [Docker and k8s](https://www.udemy.com/course/docker-kubernetes-the-practical-guide/learn/practice/1244330/summary#overview)
3. **ML Testing and Monitoring**: [ML testing notes](https://github.com/chineidu/MLOps_Tutorials/tree/main/ml_testing)
   - [Testing and Monitoring](https://www.udemy.com/course/draft/2122690/learn/lecture/17718922?start=645#overview)
4. **Spark**: [Spark notes](https://github.com/chineidu/MLOps_Tutorials/tree/main/spark_notes)
5. **GoLang**: [Go Lang](https://github.com/chineidu/MLOps_Tutorials/blob/main/main/README.md)
6. **SQL**:
   - [SQL basics](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/sql_notes/README_sql.md)
   - [SQLAlchemy](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/sql_notes/README_orm.md)
   - [Advanced SQL](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/sql_notes/ADVANCED_SQL.md)
7. **Terraform**: [Terraform](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/IaC/Terraform/README.md)
8. **MLOps**:
   - [Git](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/others/git_readme.md)
   - [Hydra And OmegaConf](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/Automations/Hydra/README.md)
   - [DVC](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/Automations/DVC/README.md)
   - [GitHub Actions](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/Automations/Github_actions/README.md)
   - [Poetry](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/Poetry/README.md)
   - [Alembic](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/Alembic_notes/README.md)
   - [Pre-commit Hooks](https://github.com/chineidu/MLOps_Tutorials/blob/main/other_notes/Automations/Pre_commit/README.md)

## Using Docker Commands

- The commands can get very long. [Docker compose](#docker-compose) can be used instead.

```shell
# Service 1
docker run -it -p 8000:8000 --rm --name cool_app \
    -v ${PWD}:/opt --network api_network mlops:v2

# Service 2
docker run -it -p 6060:6060 --rm --name serv_2 \
   -e USERNAME=neidu -e PASSWORD=password \
   --network api_network -v ${PWD}:/opt other_service:v1

# Mongo DB
docker run -itd --rm --name mongodb \
    -e MONGO_INITDB_ROOT_USERNAME=neidu \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    -v data:/data/db --network api_network mongo:7.0-rc-jammy
```

## Docker Compose

```yaml

version: "3.8"

services:
  service_1:
    build:
      context: ./
      dockerfile: Dockerfile
    image: mlops:v2
    container_name: cool_app
    ports:
      - "8000:8000"
    volumes:
      - ./:/opt # Bind mount

  service_2:
    build:
      context: ./other
      dockerfile: Dockerfile
    image: other_service:v1
    container_name: other_app
    env_file:
      - "./envs_dir/service_2.env" # Location of file containing the env vars
    ports:
      - "6060:6060"
    volumes:
      - ./other:/opt # Bind mount
    depends_on:
      - mongodb

  mongodb:
    image: mongo:7.0-rc
    container_name: mongodb
    environment:
      - MONGO_INITDB_ROOT_USERNAME=neidu
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - data:/data/db # Named volume

# Named volumes ONLY!
volumes:
  data:
```

### Mongodb String URI Format

- It can be found in the [docs](https://www.mongodb.com/docs/manual/reference/connection-string/)

```shell
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```

### Example Dockerfile

```Dockerfile
# Base image
FROM python:3.10-slim-buster

# Create working directory
WORKDIR /opt

# Copy and install dependencies. This should be here to avoid
# re-installing the packages when there's a minor change in the Docker image.
COPY ["./requirements.txt", "./"]
RUN pip install -r requirements.txt

# Copy another file
COPY ["./app.py", "./"]

# Rename the copied file (the files are already in the work_dir)
RUN mv app.py main.py

# Switch to another work_dir
WORKDIR /var/www/html

# Switch back to another work_dir
WORKDIR /opt

EXPOSE 8000

# Entry point
CMD [ "python3", "main.py", "--host", "0.0.0.0"]
```
