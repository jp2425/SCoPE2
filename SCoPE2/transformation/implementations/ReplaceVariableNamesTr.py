from random import random

from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..QueryTransformation import QueryTransformation
import re
from ..phases import Phase
from ..renameStrategy.simpleReplacement import SimpleReplacement
import random

class ReplaceVariableNamesTr(QueryTransformation):

    TRANSFORMATION_NAME: str = "generalize_vars"
    _PHASE = Phase.PROCESSING
    #the "safe" config adds after all replaced variables the special token "@TOKEN@". This is to avoid future transformations to mess with the new vars
    #however, some transformations may not like that.
    _DEFAULT_CONFIG = {"QUERY_ID":"variable", "safe":False, "replacement_probability":100}

    def __init__(self, repo_context: RepositoryContext, config: dict, **kwargs):
        self._DEFAULT_CONFIG.update(dict({"rename_strategy": SimpleReplacement()})) #default replacement strategy. Can be overwritten by the config parameter value

        self._DEFAULT_CONFIG.update(config)


        super().__init__(repo_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)
        self._repo = repo_context.tree_sitter_repo
        self.general_regex = r'(?<![a-zA-Z0-9_]){0}(?![a-zA-Z0-9_]|@TOKEN@)' #regex that covers all situations. the @TOKEN@ is used to avoid replace a string that was already replaced.


    def query(self) -> str:
        #return self._lang_repo.get_variable_names() + self._lang_repo.get_parameter_function_names()
        return self._DEFAULT_CONFIG['query']


    def remove_duplicates_list(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]


    def detect(self, entry:ProcessingEntry):
        try:
            return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]
        except:
            raise Exception("TreeSitter didn't returned any "+self._DEFAULT_CONFIG['QUERY_ID'])

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        names = self.detect(entry)
        for name in self.remove_duplicates_list(names):
            if random.random() * 100 < int(self._DEFAULT_CONFIG['replacement_probability']):
                reg = self.general_regex.replace("{0}", re.escape(name))
                if self._DEFAULT_CONFIG['safe']:
                    entry.code = re.sub(reg, self._DEFAULT_CONFIG['rename_strategy'].get_variable_name()+"@TOKEN@",
                                        entry.code)
                else:
                    entry.code = re.sub(reg, self._DEFAULT_CONFIG['rename_strategy'].get_variable_name(),
                                               entry.code)

            #self.context.code = re.sub(reg, self.generalize_service.translateVariable(name), self.context.code)
        return entry

