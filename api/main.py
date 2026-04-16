import logging
import os
from threading import Thread

from fastapi import FastAPI, BackgroundTasks
import uuid
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from join.chunk_join import join_files

app = FastAPI()


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_join(job_id: str):
    logging.info(f"Job {job_id} started")

    join_files(
        "data/users.csv",
        "data/transactions.csv",
        f"data/result_{job_id}.csv"
    )

    logging.info(f"Job {job_id} completed")


def run_join_thread(job_id: str):
    logging.info(f"[Thread] Job {job_id} started")

    join_files(
        "data/users.csv",
        "data/transactions.csv",
        f"data/result_{job_id}.csv"
    )

    logging.info(f"[Thread] Job {job_id} completed")


@app.post("/trigger-join-thread")
def trigger_join_thread():
    job_id = str(uuid.uuid4())

    thread = Thread(target=run_join_thread, args=(job_id,))
    thread.start()

    return {
        "message": "Join started using thread",
        "job_id": job_id
    }


@app.post("/trigger-join")
def trigger_join(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    background_tasks.add_task(run_join, job_id)

    return {
        "message": "Join started in background",
        "job_id": job_id
    }