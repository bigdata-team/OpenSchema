import inspect

from common.model.http import create_response
from common.repository import AsyncRepository, Repository


async def ping():
    return create_response()


async def healthz():
    return create_response()


def create_healthz(repositories: list[Repository | AsyncRepository]):
    async def healthz():
        result = {}
        for repo in repositories:
            message = "connected"
            try:
                ret = repo.connect()
                if inspect.isawaitable(ret):
                    ret = await ret
            except Exception as e:
                message = str(e)
            finally:
                name = getattr(repo, "name", repo.__class__.__name__)
                result[name] = message
        return create_response(data=result)

    return healthz
