from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..RegularTransformation import RegularTransformation
from ..phases import Phase


class NormalizeSpacingTr(RegularTransformation):
    """
    Class to normalize spacing, like spaces, tabs, newlines, etc....
    """

    TRANSFORMATION_NAME: str = "normalize_spacing"
    _PHASE = Phase.POST_PROCESSING
    _DEFAULT_CONFIG = {}

    def __init__(self, repository_context: RepositoryContext, config:dict):
        self._DEFAULT_CONFIG.update(config)
        super().__init__(repository_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)





    def run(self, entry:ProcessingEntry, remove_new_lines=False) -> ProcessingEntry:

        entry.code = self.normalize_spacing(entry.code)
        if remove_new_lines:
            entry.code = self.remove_new_lines(entry.code)
        return entry


    @staticmethod
    def normalize_spacing(code):
        return " ".join(code.split()).replace("\t", " ")

    @staticmethod
    def remove_new_lines(code):
        return code.replace("\n", "")


