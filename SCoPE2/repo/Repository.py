from abc import ABC
from ..exception.InvalidValueException import InvalidValueException

class Repository(ABC):

    def __init__(self, repository_name: str):
        if repository_name is None or repository_name == "":
            raise InvalidValueException("The repository name cannot be empty")
        self.repository_name = repository_name

