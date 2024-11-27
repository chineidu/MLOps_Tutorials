import logging

from fastapi import FastAPI
from ray import serve

# Create logger
logger = logging.getLogger(__name__)

# Create a FastAPI app
app = FastAPI(title="Demo App")


@app.get("/home")
def root() -> dict[str, str]:
    logger.info("Returning response")
    response = {"message": "Hello World!"}
    return response


# Create a Serve deployment
@serve.deployment(
    name="serve_app",
    num_replicas=2,
    ray_actor_options={"num_cpus": 0.1, "num_gpus": 0},
)
@serve.ingress(app)
class FastAPIWrapper:
    pass


serve_app = FastAPIWrapper.bind()  # type: ignore
