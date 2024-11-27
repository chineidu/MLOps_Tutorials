from fastapi import FastAPI
from ray import serve

# Create a FastAPI app
app = FastAPI()


@app.get("/home")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}


# Create a Serve deployment
@serve.deployment
@serve.ingress(app)
class FastAPIWrapper:
    pass


serve_app = FastAPIWrapper.bind()  # type: ignore
