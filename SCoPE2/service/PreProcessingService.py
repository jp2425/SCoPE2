import warnings
from typing import List, Type
from tree_sitter import Node

from .ProcessService import ProcessService
from ..config.config import transformations
from ..domain.ProcessingEntry import ProcessingEntry
from ..dto.InitialDto import InitialDto
from ..dto.PreProcessingDto import PreProcessingDto
from ..dto.ControllerServiceInitDto import ControllerServiceInitDto
from ..repo.RepositoryContext import RepositoryContext
from ..transformation.RegularTransformation import RegularTransformation
from ..transformation.QueryTransformation import QueryTransformation
from ..transformation.Transformation import Transformation
from ..transformation.phases import Phase


class PreProcessingService(ProcessService):
    """
    Class that applies the pre-processing required to the source code,
    in order to do not break any functionality with the application of regex.


    Attributes
    ----------
    code : str
        the raw source code before being parsed
    """

    def __init__(self, repo_context: RepositoryContext):
        super().__init__()
        self._repo = repo_context.tree_sitter_repo
        self.repo_context = repo_context

    def process(self, dto:InitialDto) -> PreProcessingDto:
        """
        Function to apply the pre-processing transformations to the code.

        Attributes
        ----------
        dto:ControllerServiceInitDto
            dto with the necessary information to process the code.


        Returns
        -------
        Returns the entry with the code pre-processed

        """



        entry: ProcessingEntry = ProcessingEntry(dto.code)
        entry = self._repo.parse_code(entry)


        transformations_init, query = self._initialize_transformations(dto.transformations, self._repo.language_wrapper.language_file)
        #runs the query made of all transformations sub-queries
        entry.query = query
        tokens_matches = self._repo.run_query(entry=entry, query=query)
        entry = self._repo.process_query_result(entry, tokens_matches)
        #finally, lets run the transformations that needs to be run in pre-processing phase

        entry,  transformations_init = self.run_transformation_in_phase(transformations_init,entry,Phase.PRE_PROCESSING)
        return PreProcessingDto(entry, transformations_init)



    def _initialize_transformations(self, transformations:List[Type[Transformation]], language_file_content: object) -> [List[Transformation], str]:
        """
        Function that initialize the transformations in the array.
        After the execution of this function, we will have an array with objects that apply some transformation.

        Parameters:
            transformations - list with all the classes that will be instantiated
        Returns:
            List with the transformations and the query that aggregates all the individual queries of the transformations.
        """
        transformations_init = []
        query = ""
        for transformation in transformations:
            name = transformation.TRANSFORMATION_NAME
            config = {}
            try:
                config = dict(language_file_content[name])
            except KeyError:
                pass

            if issubclass(transformation, QueryTransformation): #if the transformation is a QueryTransformation
                tr = transformation(self.repo_context,config)
                transformations_init.append(tr)
                query = query + tr.query() + "\n"
            elif issubclass(transformation, RegularTransformation):
                transformations_init.append(transformation(self.repo_context,config))
        return transformations_init, query
