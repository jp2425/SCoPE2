from .ProcessService import ProcessService
from ..dto.PreProcessingDto import PreProcessingDto
from ..dto.ProcessingDto import ProcessingDto
from ..repo.RepositoryContext import RepositoryContext
from ..transformation.phases import Phase
import warnings

class ProcessingService(ProcessService):
    def __init__(self, repo:RepositoryContext):
        super().__init__()
        self._repo = repo

    def process(self, dto_processing: PreProcessingDto) -> ProcessingDto:
        entry, transformations = self.run_transformation_in_phase(dto_processing.transformations,dto_processing.entry,Phase.PROCESSING)

        return ProcessingDto(entry, transformations)




