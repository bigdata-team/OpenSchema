from repository.info import InfoRepository

class InfoService:
    def __init__(self):
        self.repo = InfoRepository()

    def info(self):
        return self.repo.get_info()