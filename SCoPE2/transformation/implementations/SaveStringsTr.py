from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..QueryTransformation import QueryTransformation
from ..phases import Phase


class SaveStringsTr(QueryTransformation):
    """
    Class to save strings in code.
    This prevents strings to be accidentally changed by other transformations
    """

    TRANSFORMATION_NAME: str = "save_strings"
    _PHASE = Phase.PRE_PROCESSING
    _DEFAULT_CONFIG = {"QUERY_ID": "string", "QUERY_NAME": "strings"}

    def __init__(self, repo_context: RepositoryContext, config:dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)

        super().__init__(repo_context,self.TRANSFORMATION_NAME,self._PHASE,self._DEFAULT_CONFIG)
        self._repo = repo_context.tree_sitter_repo

    def run(self, entry: ProcessingEntry) -> ProcessingEntry:
        try:
            strings = entry.detection_result[self._DEFAULT_CONFIG["QUERY_ID"]]
        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])

        counter = 0
        for string in strings:
            entry.code = entry.code.replace(string, "@STRING_{0}@".format(counter))
            entry.replaced_tokens["@STRING_{0}@".format(counter)] = string
            counter += 1

        return entry

    def detect(self, entry:ProcessingEntry):
        try:
            return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]
        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])

    def query(self) -> str:
        return self._DEFAULT_CONFIG['query']

