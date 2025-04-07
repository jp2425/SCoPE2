from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..RegularTransformation import RegularTransformation
from ..phases import Phase


class RemoveTokenMarkersTr(RegularTransformation):
    """
    Class to normalize spacing, like spaces, tabs, newlines, etc....
    """

    TRANSFORMATION_NAME: str = "remove_token_markers"
    _PHASE = Phase.POST_PROCESSING
    _DEFAULT_CONFIG = {"MARKER": "@TOKEN@"}

    def __init__(self, repository_context: RepositoryContext, config: dict):
        self._DEFAULT_CONFIG.update(config)
        super().__init__(repository_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)

    def run(self, entry: ProcessingEntry) -> ProcessingEntry:
        code = entry.code
        for key in entry.replaced_tokens:
            code = code.replace(key, entry.replaced_tokens[key])

        entry.code = code.replace(self._DEFAULT_CONFIG['MARKER'], "")
        return entry
