from abc import ABC, abstractmethod
from ..domain.ProcessingEntry import ProcessingEntry
from ..repo.RepositoryContext import RepositoryContext

class Representation(ABC):

    def __init__(self, repo_context: RepositoryContext) -> None:
        super().__init__()
        self._repo_context = repo_context

    @abstractmethod
    def run(self, entry: ProcessingEntry) -> any:
        pass
