from ..repo.RepositoryContext import RepositoryContext
from .Transformation import Transformation
from .phases import Phase


class RegularTransformation(Transformation):



    def __init__(self, repository_context: RepositoryContext, transformation_name: str, transformation_phase: Phase, optional_options: dict | None) -> None:
        super().__init__(transformation_name, transformation_phase, optional_options)
        self._repository_context = repository_context



