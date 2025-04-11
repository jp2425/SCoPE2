import warnings

from .ProcessService import ProcessService
from ..config.config import transformations
from ..dto.PostProcessDto import PostProcessDto
from ..repo.RepositoryContext import RepositoryContext
from ..transformation.phases import Phase

class PostProcessService(ProcessService):

    def __init__(self, repo_context: RepositoryContext, ignore_phases = True):
        super().__init__(ignore_phases)
        self._repo = repo_context

    def process(self, dto: PostProcessDto) -> any:
        entry, _ = self.run_transformation_in_phase(dto.transformations,dto.entry,Phase.POST_PROCESSING)
        return entry


