from typing import Dict,  Any

from ..phases import Phase
from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.LanguageWrapper import LanguageWrapper
from ...repo.RepositoryContext import RepositoryContext
from ...repo.implementations.TreeSitterRepo import TreeSitterRepo
from ..QueryTransformation import QueryTransformation
import re

class ReplaceForWithWhileTr(QueryTransformation):
    """
    Class used to replace for loops with while loops
    It should be one of the first transformations to be applied to source code!! It relies on the original code to run.
    """

    TRANSFORMATION_NAME: str = "ReplaceForWithWhileTr"
    _PHASE = Phase.PRE_PROCESSING
    _DEFAULT_CONFIG = {"QUERY_ID":"for_initializer,for_condition,for_update,for_body,for_statement"}

    def __init__(self,repository_context: RepositoryContext, config: dict, **kwargs):
            self._DEFAULT_CONFIG.update(config)
            super().__init__(repository_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        entry = self._replace_for_with_while(entry)
        return entry

    def query(self) -> str:
        return self._DEFAULT_CONFIG['query']


    def _replace_for_with_while(self, entry: ProcessingEntry) -> ProcessingEntry:
        """
        Replaces all for structures with equivalent while structures,
        and substitutes variable IDs with unique ones.
        :return: code with all fors replaced with whiles
        """

        #the {0} is the initializer
        #the {1} is the condition
        # the [2} is the for body
        # the {3} is the update
        template = "{0}\nwhile({1}) {2} \n\n{3};}}"
        for_initializer_list , for_condition_list , for_update_list , for_body_list , for_statement_list = self.detect(entry=entry)

        for for_structure in list(for_statement_list):
            id_for = for_statement_list.index(for_structure)
            # Created the while loop using the template defined above
            new_while = template.format(for_initializer_list[id_for], for_condition_list[id_for], for_body_list[id_for][:-1], #remove the first line of the for body (its the for declaration)
                                        for_update_list[id_for].replace(",", ";"))
            # We need to store the new structure to replace the old "for" with the new while
            entry.code = entry.code.replace(for_structure, new_while)

        return entry



    def detect(self, entry: ProcessingEntry) :

        try:
            for_initializer,for_condition,for_update,for_body,for_statement = self._DEFAULT_CONFIG['QUERY_ID'].split(",")
            return entry.detection_result[for_initializer], entry.detection_result[for_condition], entry.detection_result[for_update], entry.detection_result[for_body], entry.detection_result[for_statement]
        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])


