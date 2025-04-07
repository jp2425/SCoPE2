import re

import warnings

from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.RepositoryContext import RepositoryContext
from ..QueryTransformation import QueryTransformation
from ..phases import Phase


class SwapOperatorsTr(QueryTransformation):
    """
    Class to swap operators in code.
    """

    TRANSFORMATION_NAME: str = "swap_operators"
    _PHASE = Phase.PROCESSING
    _DEFAULT_CONFIG = {"QUERY_ID": "swap_expressions"}

    def __init__(self, repo_context: RepositoryContext, config:dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)

        super().__init__(repo_context,self.TRANSFORMATION_NAME,self._PHASE,self._DEFAULT_CONFIG)
        self._repo = repo_context.tree_sitter_repo

    def run(self, entry: ProcessingEntry) -> ProcessingEntry:
        expressions = entry.detection_result[self._DEFAULT_CONFIG["QUERY_ID"]]
        supported_operators = self._DEFAULT_CONFIG["SUPPORTED_OPERATORS"]
        temp = sorted(supported_operators, key=len, reverse=True)
        regex_ops = '|'.join(re.escape(op) for op in temp)
        padrao = rf'^\s*(\S+)\s*({regex_ops})\s*(\S+)\s*$'


        counter = 0
        for expression in expressions:
            match = re.match(padrao, expression)
            if match:
                print(match)
                x, operator, y = match.groups()
                X, new_op, Y = self.swap_operator(x,operator, y)
                entry.code = entry.code.replace(expression, str(X)+" "+str(new_op)+" "+str(Y))
            else:
                warnings.warn("["+self.TRANSFORMATION_NAME+"] One value returned from treesitter is not being accounted for in the transformation. This case won't be touched by the transformation so the code is still correct.")
        #    entry.code = entry.code.replace(string, "@STRING_{0}@".format(counter))
        #    entry.replaced_tokens["@STRING_{0}@".format(counter)] = string
        #    counter += 1

        return entry


    def swap_operator(self, X, operator, Y):
        if operator == ">":
            # X > Y
            return Y, "<", X
        if operator == "<":
            # X < Y
            return Y, ">", X
        if operator == ">=":
            # X >= Y
            return Y ,"<=", X
        if operator == "<=":
            # X <= Y
            return Y, ">=", X
        return X, operator, Y

    def detect(self, entry:ProcessingEntry):
        try:
            return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]
        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])

    def query(self) -> str:

        return self._DEFAULT_CONFIG['query']

