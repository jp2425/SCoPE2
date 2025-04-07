from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..QueryTransformation import QueryTransformation
import re
from ..phases import Phase
from ..renameStrategy.simpleReplacement import SimpleReplacement


class ReplaceFunctionNamesTr(QueryTransformation):

    TRANSFORMATION_NAME: str = "generalize_functions"
    _PHASE = Phase.PROCESSING
    _DEFAULT_CONFIG:dict = {"QUERY_ID":"function"}

    def __init__(self, repository_context: RepositoryContext, config: dict, **kwargs):

        self._DEFAULT_CONFIG.update(dict({"rename_strategy": SimpleReplacement()}))
        self._DEFAULT_CONFIG.update(config)
        super().__init__(repository_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)
        self._repo = repository_context.tree_sitter_repo
        self.regex_function = r"(?<=[ *(:]){0}(?=[( ]+(\( )?)|^{0}(?=[( ]+(\( )?)"


    def detect(self, entry:ProcessingEntry) -> list:
        try:
            return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]
        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])

    def query(self) -> str:
        return self._DEFAULT_CONFIG['query']

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        for name in self.detect(entry):
            reg = self.regex_function.replace("{0}", re.escape(name))

            entry.code = re.sub(reg, self._DEFAULT_CONFIG['rename_strategy'].get_function_name() + "@TOKEN@",
                                entry.code)
            # entry.code = re.sub(reg, self.generalize_service.translateVariable(name), entry.code)
        return entry

