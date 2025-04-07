from ..domain.ProcessingEntry import ProcessingEntry
from ..repo.RepositoryContext import RepositoryContext
from .Representation import Representation


class CodeRepresentation(Representation):
    def __init__(self, repo_context: RepositoryContext):
        super().__init__(repo_context)

    def run(self, entry: ProcessingEntry) -> any:
        return entry.code