from typing import Any, Dict

from repository.info import InfoRepository


class InfoService:
    def __init__(self):
        self.repo = InfoRepository()

    def info(self):
        return self.repo.get_info()

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and return result"""
        # Example processing logic
        processed_data = {
            "original_data": data,
            "processed_at": "2025-10-02",
            "status": "success",
        }
        return processed_data
