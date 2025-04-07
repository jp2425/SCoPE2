from abc import  abstractmethod
from ..domain.ProcessingEntry import ProcessingEntry
from ..repo.RepositoryContext import RepositoryContext
from .Transformation import Transformation
from .phases import Phase


class QueryTransformation(Transformation):

    def __init__(self, repository_context: RepositoryContext, transformation_name: str, transformation_phase: Phase, optional_settings: dict | None) -> None:
        super().__init__(transformation_name,transformation_phase,optional_settings)
        self._repository_context = repository_context

    @abstractmethod
    def run(self, entry: ProcessingEntry) -> ProcessingEntry:
        '''
        This method will implement the logic of the transformation
        :return:
        '''
        pass

    @abstractmethod
    def query(self) -> str:
        '''
        Method used to get the query related to the transformation.

        '''
        pass


