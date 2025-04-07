from ..RegularTransformation import RegularTransformation
from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..phases import Phase
from random import randint
import re

class DeadCodeInjection(RegularTransformation):

    TRANSFORMATION_NAME: str = "dead_code_injection"
    _PHASE = Phase.POST_PROCESSING

    _DEFAULT_CONFIG = {"dead_code":["int alkdlp = 0;", "if(1==2){\n int test = 0;\n printf(\"%d\", test);}\n}"]}

    def __init__(self, repo_context: RepositoryContext, config: dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)
        super().__init__(repo_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)


    def has_semicolon(self, text):
        lines = text.split('\n')
        for line in lines:
            if line.strip().endswith(';'):
                return True
        return False

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:

        number_of_lines = len(entry.code.splitlines())

        has_semicolon = self.has_semicolon(entry.code)
        if not has_semicolon:
            raise Exception("No semicolon detected on code.")
        while True:
            line_number = randint(0, number_of_lines - 1)
            ends_with_semicolon = entry.code.splitlines()[line_number].strip().endswith(";")
            if ends_with_semicolon:
                dead_code = self._DEFAULT_CONFIG["dead_code"][randint(0, len(self._DEFAULT_CONFIG["dead_code"])-1)]
                entry.code = entry.code.replace(entry.code.splitlines()[line_number],
                                                entry.code.splitlines()[line_number] +"\n"+ dead_code)
                break

        return entry

