from ...domain.ProcessingEntry import ProcessingEntry
from ...exception.IncompatibleTransformation import IncompatibleTransformation
from ...repo.RepositoryContext import RepositoryContext
from ...repo.implementations.TreeSitterRepo import TreeSitterRepo
from ..QueryTransformation import QueryTransformation
from ..phases import Phase


class SaveCommentsTr(QueryTransformation):


    """
    Class to save comments from code.
    It also contains auxiliary methods to process comments.

    Attributes
    ----------
    repo: TreeSitterRepo
        repository to interact with treesitter
    """

    TRANSFORMATION_NAME: str = "save_comments"
    _PHASE = Phase.PRE_PROCESSING
    _DEFAULT_CONFIG = {"SAVED_COMMENTS_CONTEXT_KEY": "SAVED_COMMENTS", "QUERY_ID": "comment"}

    def __init__(self, repo_context: RepositoryContext, config:dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)

        super().__init__(repo_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)
        self._repo = repo_context.tree_sitter_repo

    def _validate_previous_transformations(self, entry: ProcessingEntry):
        """
        We don't want to run this transformation if the remove comment transformation was added
        :param entry: processing entry
        """

        if "remove_comments" in entry.transformations_applied:
            raise IncompatibleTransformation("This transformation should not be ran after the "+"remove_comments"+" transformation")

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        """
        Function to replace the comments in  code stored in the context.
        """

        self._validate_previous_transformations(entry)
        comments = self.detect(entry)
        counter = 0
        for comment in comments:
            entry.code = entry.code.replace(comment, "/*@COMMENT_{0}@*/".format(counter))
            entry.replaced_tokens["/*@COMMENT_{0}@*/".format(counter)] = comment
            counter += 1

        return entry

    def query(self) -> str:
        #return self._lang_repo.get_query_comments()
        return self._DEFAULT_CONFIG['query']

    def detect(self, entry:ProcessingEntry) -> list:
        try:
            return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]

        except:
            raise Exception("TreeSitter didn't returned any " + self._DEFAULT_CONFIG['QUERY_ID'])



