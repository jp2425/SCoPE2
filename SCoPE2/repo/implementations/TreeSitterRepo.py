from typing import List
from tree_sitter import Parser, Tree, Node
from ...domain.ProcessingEntry import ProcessingEntry
from ...dto.ForStructureRepoServiceDto import ForStructureRepoServiceDto
from ..LanguageWrapper import LanguageWrapper
from ..Repository import Repository


class TreeSitterRepo(Repository):
    """
    Class responsible to handle with treesitter.
    It uses the query file wrapper to get the queries used to extract the code elements for the application of code transformations.
    """
    
    _LEAVE_WHITELIST = {"identifier", "integer", "float"}


    def __init__(self, language_wrapper: LanguageWrapper):
        super().__init__(repository_name="tree_sitter_repo")
        self._parser = Parser(language_wrapper.language)
        self.language_wrapper= language_wrapper


    def run_query(self, entry: ProcessingEntry, query:str ) -> list[tuple[int, dict[str, list[Node]]]]:
        if query == "":
            raise ValueError("Query cannot be empty")

        return self.language_wrapper.language.query(query).matches(entry.tree.root_node)

    def parse_code(self, entry:ProcessingEntry) -> ProcessingEntry:
        entry.tree = self._parser.parse(bytes(entry.code, 'utf-8'))
        return entry

    def process_query_result(self, entry: ProcessingEntry, token_matches:list[tuple[int, dict[str, list[Node]]]]) -> dict[str: list]:
        values:dict[str: list] = {}
        for value in token_matches:
            for value2 in value[1].keys():
                if value2 in values.keys():
                    values[value2].append(value[1][value2][0].text.decode('utf-8'))
                else:
                    values[value2] = [value[1][value2][0].text.decode('utf-8')]
        entry.detection_result = values
        return entry

    def get_tokens(self, node: Node) -> list:
        tokens = []
        for n in node.children:
            if n.child_count == 0:
                tokens.append(n.text.decode())
            else:
                if (n.text.decode().startswith("\"") and n.text.decode().endswith('"')) or (
                        n.text.decode().startswith("\'") and n.text.decode().endswith(
                        "\'")):  # we want to capture the whole string as a unique token
                    tokens.append(n.text.decode())
                else:
                    tokens_temp = self.get_tokens(n)
                    if tokens_temp:
                        tokens += tokens_temp
        return tokens

    '''def get_function_names(self, tree:Tree, query_function_names:str) -> List[str]:
        query = self.language_wrapper.language.query(query_function_names)
        names:List[str] = []
        for match in query.matches(tree.root_node):
            names.append(str(match[1]['function'][0].text.decode('utf-8')))
        return names


    def get_parameters_function_names(self, tree: Tree, query_parameter_function_names:str) -> List[str]:
        query = self.language_wrapper.language.query(query_parameter_function_names)
        names: List[str] = []
        for match in query.matches(tree.root_node):
            names.append(str(match[1]['variable.parameter'][0].text.decode('utf-8')))
        return names


    def get_variable_names(self, tree: Tree, query_variable_names:str) -> List[str]:
        query = self.language_wrapper.language.query(query_variable_names)
        names: List[str] = []
        for match in query.matches(tree.root_node):
           names.append(str(match[1]['variable'][0].text.decode('utf-8')))
        return names

    def get_strings(self, tree: Tree, query_strings:str) -> List[str]:
        query = self.language_wrapper.language.query(query_strings)
        comments: List[str] = []
        for match in query.matches(tree.root_node):
            comments.append(str(match[1]['string'][0].text.decode('utf-8')))
        return comments

    def get_comments(self, tree: Tree, query_comments: str) -> List[str]:
        query =  self.language_wrapper.language.query(query_comments)
        comments : List[str] = []
        for match in query.matches(tree.root_node):
            comments.append(str(match[1]['comment'][0].text.decode('utf-8')))
        return comments'''

    def get_for_structures(self, tree: Tree, for_repetition_structures_query:str) -> List[ForStructureRepoServiceDto]:
        query = self.language_wrapper.language.query(for_repetition_structures_query)

        # Dicionário para agrupar as partes do 'for', mas var_ids será uma lista
        grouped_fors = {}

        # Conjunto para rastrear estruturas 'for' já processadas
        processed_for_structures = set()

        # Executa a query para encontrar as correspondências
        for match in query.matches(tree.root_node):

            for_structure_key = str(match[1]['for_structure'][0].text.decode('utf-8'))

            # If the for was already processed (we can have the same for in the code multiple times) we don't need to process it
            if for_structure_key in processed_for_structures:
                continue

            processed_for_structures.add(for_structure_key)

            grouped_fors[for_structure_key] = {
                'declaration': str(match[1]['declaration'][0].text.decode('utf-8')),
                'condition': str(match[1]['condition'][0].text.decode('utf-8')),
                'update': str(match[1]['update'][0].text.decode('utf-8')),
                'body': str(match[1]['body'][0].text.decode('utf-8')),
                'var_ids': [str(match[1]['var_id'][0].text.decode('utf-8'))]  # can have multiple IDs
            }

        # Create the DTOs
        result = []
        for for_structure, elements in grouped_fors.items():
            result.append(ForStructureRepoServiceDto(
                for_structure=for_structure,
                declaration=elements['declaration'],
                condition=elements['condition'],
                update=elements['update'],
                body=elements['body'],
                var_ids=elements['var_ids']
            ))

        return result

    def _serialize_node(self, node) -> str:
        """
        Gets the string representation of a node.
        :param node: node to serialize
        :return: string representing the node
        """

        return f"{node.type} [{node.start_point[0]}, {node.start_point[1]}] - [{node.end_point[0]}, {node.end_point[1]}]"

    def ast_to_str(self, tree, indent=0):
        """
        Gets the string representation of an AST.
        From https://github.com/cedricrupb/code_ast/tree/main/code_ast
        Usage: ast_to_str(tree)

        :param tree: branch to visit
        :param indent: for printing purposes
        :return: the string representation of an AST
        """

        ast_lines = []
        root_node = tree.root_node
        cursor = root_node.walk()

        has_next = True

        while has_next:
            current_node = cursor.node

            if current_node.child_count > 0 or current_node.type in self._LEAVE_WHITELIST:
                ast_lines.append("    " * indent + self._serialize_node(current_node))

            # Step 1: Try to go to next child if we continue the subtree
            if cursor.goto_first_child():
                indent += 1
                has_next = True
            else:
                has_next = False

            # Step 2: Try to go to next sibling
            if not has_next:
                has_next = cursor.goto_next_sibling()

            # Step 3: Go up until sibling exists
            while not has_next and cursor.goto_parent():
                indent -= 1
                has_next = cursor.goto_next_sibling()

        return "\n".join(ast_lines)

