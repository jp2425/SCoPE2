import tree_sitter_cpp
from tree_sitter import Language

from dto.ControllerServiceInitDto import ControllerServiceInitDto
from dto.PostProcessDto import PostProcessDto
from repo.LanguageWrapper import LanguageWrapper
from repo.implementations.TreeSitterRepo import TreeSitterRepo
from service.PostProcessService import PostProcessService
from service.PreProcessingService import PreProcessingService
from service.ProcessingService import ProcessingService
from transformation.renameStrategy.minifyReplacement import MinifyReplacement
from transformation.renameStrategy.simpleReplacement import SimpleReplacement

import time

class ProcessCodeController:

    def __int__(self):
        pass

    def processCode(self, requestJson):
        generalize_functions = requestJson['generalizeFunctionNames']
        generalize_variables = requestJson['generalizeVariableNames']
        generalize_strings = requestJson['generalizeStrings']
        returnType = requestJson['returnType']
        replacementStrategy = None
        if int(requestJson['replacementStrategy'] == 1):
            replacementStrategy = MinifyReplacement()
        else:
            #default
            replacementStrategy = SimpleReplacement()

        start = time.time()
        dto = ControllerServiceInitDto(code=requestJson['code'],
                                       remove_comments=True,
                                       generalize_strings=bool(generalize_strings),
                                       generalize_functions=bool(generalize_functions),
                                       generalize_vars=bool(generalize_variables),
                                       return_type=int(returnType),
                                       replace_strategy=replacementStrategy,
                                       replace_equivalent_values=False,
                                       normalize_spacing=False,
                                       prettify_code=False)
        repo2 = LanguageWrapper(r"query/cpp.yaml")
        repo = TreeSitterRepo(repo2, Language(tree_sitter_cpp.language()))
        start = time.time()
        start_pre_processing = time.time()
        out = PreProcessingService(repo, repo2).process(dto)
        stop_pre_processing = time.time()

        out2 = ProcessingService(repo).process(out)
        value = PostProcessService(repo, repo2).process(PostProcessDto(out2.entry, int(returnType), out2.transformations))


        end = time.time()
        print(value)

        print()
        print("[*] Estatísticas:")
        print("Tempo de execução: ", end-start)
        print("Tokens processados: ", len(value))
        print("\n\n")
        return value
