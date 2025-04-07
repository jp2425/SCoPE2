import unittest

import tree_sitter_cpp
from tree_sitter import Language

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.repo.LanguageWrapper import LanguageWrapper
from SCoPE2.repo.RepositoryContext import RepositoryContext
from SCoPE2.repo.implementations.TreeSitterRepo import TreeSitterRepo
from SCoPE2.transformation.implementations.SaveStringsTr import SaveStringsTr


class SaveStringsTrTest(unittest.TestCase):
    yaml_file_content = """
    save_strings:
        query: (string_literal) @string ;the node 'string_content' gives the content of the string
        QUERY_ID: string
    """

    def test_simple1(self):
        code = r"""
        int test_simple_replacement(){
            int test1, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", test1, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = SaveStringsTr(context, repo2.language_file[SaveStringsTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code)
        assert entry.code == r"""
        int test_simple_replacement(){
            int test1, test2 ,test3 = 0;
            char test_string[] = @STRING_0@;
            printf(@STRING_1@, test1, test2, test3);
            printf(@STRING_2@, test_string);
            return 0;
        }
        """
        print(entry.replaced_tokens)
        assert entry.replaced_tokens["@STRING_0@"] == '"hello world!\\n"'
        assert entry.replaced_tokens["@STRING_1@"] == '"%d, %d, %d, %d\\n"'
        assert entry.replaced_tokens["@STRING_2@"] == '"%s\\n"'

