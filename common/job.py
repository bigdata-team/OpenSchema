from celery import shared_task


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_kwargs={"max_retries": 3},
)
def pseudo(self, payload: dict) -> dict:
    return payload
