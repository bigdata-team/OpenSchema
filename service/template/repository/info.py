import os
from common.repository import Repository


class InfoRepository(Repository):
    def __init__(self):
        self.service_id = os.getenv("SERVICE_ID")
        self.service_name = os.getenv("SERVICE_NAME")

    def get_info(self):
        return {
            "service_id": self.service_id,
            "service_name": self.service_name
        }