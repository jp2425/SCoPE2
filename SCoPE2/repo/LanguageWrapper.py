from ruamel.yaml import YAML
from io import StringIO
from tree_sitter import Language


class LanguageWrapper:
    """
    This wrapper is responsible to get the queries used in the processing phase.
    The queries are used with treesitter to get elements of the AST
    """


    def __init__(self, query:str, language:Language):
        self.language_file = None
        self.language = language

        yaml = YAML(typ='safe', pure=True)

        #if os.path.exists(os.path.normpath(query_path)):
        #    file = open(os.path.normpath(query_path))
        #    self.language_file = yaml.load(file)
        #    file.close()
        #else:
        #    raise Exception("Query file does not exist")
        self.language_file = yaml.load(StringIO(query))

    def get_query_comments(self) -> str:
        return self.language_file['queries']['comments']['query']

    def get_query_strings(self) -> str:
        return self.language_file['queries']['strings']['query']

    def get_query_function_names(self) -> str:
        return self.language_file['queries']['function_names_declaration']['query']

    def get_parameter_function_names(self) -> str:
        return self.language_file['queries']['parameter_names_function_declaration']['query']


    def get_variable_names(self) -> str:
        return self.language_file['queries']['variable_names_declaration']['query']

    def get_for_repetition_structures(self) -> str:
        return self.language_file['queries']['repetition_structures']['for_structure']['query']

    def get_while_repetition_structures(self) -> str:
        return self.language_file['queries']['repetition_structures']['while_structure']['query']

    def get_replacement_regex(self) ->str:
        return self.language_file['replace_regex']['regex']

    def get_infinite_for_regex_replacement(self) ->[str, str]:
        """
        :return: [ the regex used to replace the infinite for : the value used to replace the old one ]
        """
        return [self.language_file['infinite_for_regex_replacement']['regex'], self.language_file['infinite_for_regex_replacement']['replace_by']]

    def get_literal_replace(self) -> {str:str}:

        return self.language_file['replacer']['literals']
