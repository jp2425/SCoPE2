from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..RegularTransformation import RegularTransformation
from ..phases import Phase


class ReParseCodeAx(RegularTransformation):
    """
    Auxiliary Class to re parse the code in a transformation.
    It is usefull when a specific transformation needs updated code information. Like when it needs to do a replacement in a block of code using
    the data returned from the parser. If other transformation already changed that block, the information will be outdated. So a re-parse is needed
    """

    TRANSFORMATION_NAME: str = "reparsecodeAx"
    _PHASE = Phase.ANY
    _DEFAULT_CONFIG = {}

    def __init__(self, repository_context: RepositoryContext, config:dict):
        self._DEFAULT_CONFIG.update(config)
        super().__init__(repository_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)

    def run(self, entry:ProcessingEntry, remove_new_lines=False) -> ProcessingEntry:
        entry  = self._repository_context.tree_sitter_repo.parse_code(entry)
        tokens_matches = self._repository_context.tree_sitter_repo.run_query(entry=entry, query=entry.query)
        entry = self._repository_context.tree_sitter_repo.process_query_result(entry, tokens_matches)
        return entry


