from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..RegularTransformation import RegularTransformation
from ..phases import Phase


class ReplaceLiteralsEquivalentValuesTr(RegularTransformation):

    TRANSFORMATION_NAME: str = "replace_equivalent_values"
    _PHASE = Phase.PROCESSING
    _DEFAULT_CONFIG = {"literals":{"true":"1==1", "false": "1==2"}}



    def __init__(self, repository_context: RepositoryContext, config:dict):
        self._DEFAULT_CONFIG.update(config)

        super().__init__(repository_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)


    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        dict_replace: dict = self._DEFAULT_CONFIG["literals"]
        for key in dict_replace:
            entry.code = entry.code.replace(str(key), dict_replace[key])

        return entry

