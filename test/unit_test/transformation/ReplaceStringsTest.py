import unittest

import tree_sitter_cpp
from tree_sitter import Language

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.repo.LanguageWrapper import LanguageWrapper
from SCoPE2.repo.RepositoryContext import RepositoryContext
from SCoPE2.repo.implementations.TreeSitterRepo import TreeSitterRepo
from SCoPE2.transformation.implementations.ReplaceStringsTr import ReplaceStringsTr
from SCoPE2.transformation.renameStrategy.minifyReplacement import MinifyReplacement


class ReplaceStringsTest(unittest.TestCase):
    yaml_file_content = """
    generalize_strings:
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
        tr = ReplaceStringsTr(context, repo2.language_file[ReplaceStringsTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code)
        assert entry.code == r"""
        int test_simple_replacement(){
            int test1, test2 ,test3 = 0;
            char test_string[] = STRING_TOKEN;
            printf(STRING_TOKEN, test1, test2, test3);
            printf(STRING_TOKEN, test_string);
            return 0;
        }
        """
    def test_simple2(self):
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
        v = dict(repo2.language_file[ReplaceStringsTr.TRANSFORMATION_NAME])
        v.update({"rename_strategy": MinifyReplacement()})
        tr = ReplaceStringsTr(context, v)
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code)
        assert entry.code == r"""
        int test_simple_replacement(){
            int test1, test2 ,test3 = 0;
            char test_string[] = S;
            printf(S, test1, test2, test3);
            printf(S, test_string);
            return 0;
        }
        """
