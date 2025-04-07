
import time
import tree_sitter_cpp
from tree_sitter import Language

from dto.ControllerTransformationListDto import ControllerTransformationListDto
from dto.PostProcessDto import PostProcessDto
from dto.ControllerServiceInitDto import ControllerServiceInitDto
from main2 import lang_repo
from repo.LanguageWrapper import LanguageWrapper
from repo.RepositoryContext import RepositoryHolder
from repo.implementations.TreeSitterRepo import TreeSitterRepo
from service.PostProcessService import PostProcessService
from service.PreProcessingService import PreProcessingService
from service.ProcessingService import ProcessingService
from transformation.renameStrategy.simpleReplacement import SimpleReplacement


class TestController:

    def __int__(self):
        pass

    def processCode(self):
        code = r"""

        // Função para resolver o Sudoku usando backtracking
bool resolveSudoku(int grid[N][N], int *row = 0, int col = 0) {

    char teste[] = "teste string";
    // Se chegamos à última célula, o Sudoku está resolvido
    if (row == N - 1 && col == N)
        return true;

    // Se a coluna chegou ao final, passar para a próxima linha
    if (col == N) {
        row++;
        col = 0;
    }

    // Se a célula já contém um número, ir para a próxima célula
    if (grid[row][col] != 0)
        return resolveSudoku(grid, row, col + 1);

    // Tentar os números de 1 a 9
    for (int num = 1; num <= 9; num++) {
        // Verificar se o número pode ser colocado na célula atual
        bool seguro = true;
        for (int x = 0; x < N; x++) {
            // Verificar linha, coluna e subgrid 3x3
            if (grid[row][x] == num || grid[x][col] == num ||
                grid[row - row % 3 + x / 3][col - col % 3 + x % 3] == num) {
                seguro = false;
                break;
            }
        }

        // Se o número é seguro, colocá-lo
        if (seguro) {
            grid[row][col] = num;

            // Recursivamente tentar resolver o restante do tabuleiro
            if (resolveSudoku(grid, row, col + 1))
                return true;
        }

        // Se o número não levou a uma solução, removê-lo
        grid[row][col] = 0;
    }

    return false; // Nenhum número levou a uma solução, retornar falso
}
        """
        replacementStrategy = SimpleReplacement()
        transf = ControllerTransformationListDto(remove_comments=True,
                                                 save_comments = False,
                                                 save_strings = False,
                                       generalize_strings=True,
                                       generalize_functions=True,
                                       generalize_vars=True,
                                        replace_equivalent_values=False,
                                        normalize_spacing=False,
                                        prettify_code=False)
        dto = ControllerServiceInitDto(code=code,
                                       return_type=1,
                                       replace_strategy=replacementStrategy,
                                       transformations = transf
                                       )
        repo2 = LanguageWrapper(r"query/cpp.yaml",Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        start = time.time()
        repo_context = RepositoryHolder(repo)
        start_pre_processing = time.time()
        out = PreProcessingService(repo_context,repo2).process(dto)
        stop_pre_processing = time.time()

        out2 = ProcessingService(repo).process(out)
        value = PostProcessService(repo, lang_repo).process(PostProcessDto(out2.entry, 1, out2.transformations))
        print(value)

        end = time.time()
        print("Tempo de execução pré-processamento: ", stop_pre_processing-start_pre_processing)

        print("[*] Estatísticas:")
        print("Tempo de execução: ", end-start)
        print("\n\n")
