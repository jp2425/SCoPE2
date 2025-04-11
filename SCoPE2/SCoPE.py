import time
from typing import Type, List

from tree_sitter import Language

from .dto.InitialDto import InitialDto
from .dto.PostProcessDto import PostProcessDto
from .repo.LanguageWrapper import LanguageWrapper
from .repo.Repository import Repository
from .repo.RepositoryContext import RepositoryContext
from .repo.implementations.TreeSitterRepo import TreeSitterRepo
from .representations.Representation import Representation
from .service.PostProcessService import PostProcessService
from .service.PreProcessingService import PreProcessingService
from .service.ProcessingService import ProcessingService
from .transformation.Transformation import Transformation


class SCoPE:

    def __init__(self, query_path: str, language: Language):
        language_wrapper = LanguageWrapper(query_path, language)
        tree_sitter_repo = TreeSitterRepo(language_wrapper)
        self._repository_context = RepositoryContext(tree_sitter_repo)


    def add_repo(self, repository: Repository):
        """
        Function to add the repository to the repository context
        :param repository: Repository instance to add to the context.
        """
        self._repository_context.add_repo(repository)

    def process(self, code: str, transformation_list: List[Type[Transformation]], representation: Type[Representation], ignore_phases = True) -> any:
        """
       Function that applies transformations to the source code.
      :param code: code to process
      :param transformation_list: list of all transformations to apply. They should not be initialized!
      :param representation: the final representation of the code. It should not be initialized!
      :param transformation_settings: settings to be passed to the transformations. It should be in the format {"transformation_name": {"key", "value"}, "transformation_name": {"key","value"}}}.
      :return: the processed code.
      """

        dto = InitialDto(code, transformation_list)
        out = PreProcessingService(self._repository_context, ignore_phases).process(dto)
        out2 = ProcessingService(self._repository_context, ignore_phases).process(out)
        ent = PostProcessService(self._repository_context, ignore_phases).process(PostProcessDto(out2.entry, out2.transformations))
        value = representation(self._repository_context).run(ent)

        return value