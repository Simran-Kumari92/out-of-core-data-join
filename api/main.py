from fastapi import FastAPI, BackgroundTasks
import uuid
import sys
import os

# Fix import path (IMPORTANT)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from join.chunk_join import join_files

app = FastAPI()


def run_join(job_id: str):
    print(f"🚀 Job {job_id} started")

    join_files(
        "data/users.csv",
        "data/transactions.csv",
        f"data/result_{job_id}.csv"
    )

    print(f"✅ Job {job_id} completed")


@app.post("/trigger-join")
def trigger_join(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    background_tasks.add_task(run_join, job_id)

    return {
        "message": "Join started in background",
        "job_id": job_id
    }