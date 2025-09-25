import json
from common.connection.redis import get_redis
from common.utils import Now
import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
CELERY_REDIS_DB = os.getenv("CELERY_REDIS_DB")


redis = get_redis(host=REDIS_HOST, port=REDIS_PORT, db=CELERY_REDIS_DB)


def set_status(job_id: str, phase: str, state: str, extra: dict = {}):
    now = Now().ts
    key = f"job:{job_id}"
    payload = {"job_id": job_id, "phase": phase, "state": state, "ts": now, **extra}
    payload_string = json.dumps(payload)
    redis.set(key, payload_string)
    redis.publish("job.status", payload_string)
    return payload
