from .Repository import Repository
from .implementations.TreeSitterRepo import TreeSitterRepo


class RepositoryContext:

    def __init__(self, tree_sitter_repo: TreeSitterRepo, extra_repos: dict = None):
        self.tree_sitter_repo = tree_sitter_repo
        self.extra_repos = extra_repos or {}

    def add_repo(self, repository: Repository):
        self.extra_repos[repository.repository_name] = repository
    def get_repo(self, name: str) -> object|None:
        """ get repository by name, if it exists. Otherwise, returns none """
        return self.extra_repos.get(name, None)

