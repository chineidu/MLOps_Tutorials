# MLOps_Tutorials

This course contains tutorials for Docker, K8s, Model deployment, etc.

This course was inspired by the following Udemy courses:

1. **Docker**: [Docker](https://www.udemy.com/course/docker-kubernetes-the-practical-guide/learn/practice/1244330/summary#overview)
2. **Kubernetes**: [k8s](https://www.udemy.com/course/docker-kubernetes-the-practical-guide/learn/practice/1244330/summary#overview)

## Commands Used

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

### Mongodb String URI Format

- It can be found in the [docs](https://www.mongodb.com/docs/manual/reference/connection-string/)

```shell
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```
