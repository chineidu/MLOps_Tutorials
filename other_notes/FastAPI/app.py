import asyncio
import random
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, Response, status

app = FastAPI()

# in-memory store: job_id -> {"status": "running"|"completed"|"failed"}
jobs: dict[str, dict] = {}


# 1. Client calls this to kick off the long job
@app.post("/task", status_code=status.HTTP_202_ACCEPTED)
async def start_task(resp: Response, background: BackgroundTasks):
    job_id = str(uuid4())
    jobs[job_id] = {"status": "running"}

    background.add_task(_do_work, job_id)  # FastAPI runs it in the thread-pool

    resp.headers["Location"] = f"/status/{job_id}"
    return {"message": "job accepted", "job_id": job_id}


# 2. Client polls this URI (value of the Location header)
@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return Response(status_code=404)
    return job


# dummy background worker
async def _do_work(job_id: str):
    await asyncio.sleep(random.randint(5, 10))  # pretend to work
    jobs[job_id]["status"] = "completed"


# keep your old health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
