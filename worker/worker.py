import redis
import time
import os
import signal
import sys

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)

running = True


def handle_shutdown(signum, frame):
    global running
    print("Shutdown signal received, stopping worker...")
    running = False


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


if __name__ == "__main__":
    print(f"Worker started, connecting to Redis at {REDIS_HOST}:{REDIS_PORT}")
    while running:
        try:
            job = r.brpop("job", timeout=5)
            if job:
                _, job_id = job
                process_job(job_id)
        except redis.exceptions.ConnectionError as e:
            print(f"Redis connection error: {e}. Retrying in 3s...")
            time.sleep(3)
    print("Worker stopped cleanly.")
    sys.exit(0)
