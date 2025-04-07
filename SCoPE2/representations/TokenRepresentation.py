from ..domain.ProcessingEntry import ProcessingEntry
from ..repo.RepositoryContext import RepositoryContext
from .Representation import Representation

class TokenRepresentation(Representation):
    def __init__(self, repository_context: RepositoryContext):
        super().__init__(repository_context)

    def run(self, entry: ProcessingEntry) -> any:
        entry = self._repo_context.tree_sitter_repo.parse_code(entry)
        return self._repo_context.tree_sitter_repo.get_tokens(entry.tree.root_node)


