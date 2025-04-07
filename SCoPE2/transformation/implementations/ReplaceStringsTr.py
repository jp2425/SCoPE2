from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..QueryTransformation import QueryTransformation
from ..phases import Phase
from ..renameStrategy.simpleReplacement import SimpleReplacement


class ReplaceStringsTr(QueryTransformation):


    """
    Class to remove comments from code.
    It also contains auxiliary methods to process comments.

    Attributes
    ----------
    entry: ProcessingEntry
        Entity representing the code
    """

    TRANSFORMATION_NAME: str = "generalize_strings"
    _PHASE = Phase.PRE_PROCESSING
    _DEFAULT_CONFIG = {"QUERY_ID": "string", "rename_strategy": SimpleReplacement()}

    def __init__(self, repo_context: RepositoryContext, config:dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)

        super().__init__(repo_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)
        self._repo = repo_context.tree_sitter_repo

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        """Replaces strings with a generic token"""

        strings = self.detect(entry)
        for string in strings:
            entry.code =entry.code.replace(string,
                                            self._DEFAULT_CONFIG['rename_strategy'].get_string_replacer())
        return entry

    def query(self) -> str:
        return self._DEFAULT_CONFIG['query']

    def detect(self, entry:ProcessingEntry) -> list:
        try:
            return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]
        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])
