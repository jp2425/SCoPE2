import unittest

import tree_sitter_cpp
from tree_sitter import Language

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.repo.LanguageWrapper import LanguageWrapper
from SCoPE2.repo.RepositoryContext import RepositoryContext
from SCoPE2.repo.implementations.TreeSitterRepo import TreeSitterRepo
from SCoPE2.transformation.implementations.RemoveCommentsTr import RemoveCommentsTr
from SCoPE2.transformation.implementations.RemoveTokenMarkersTr import RemoveTokenMarkersTr


class RemoveCommentsTrTest(unittest.TestCase):

    def test_simple1(self):
        code = r"""
        int FUNC0@TOKEN@(){
            int test1, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", test1, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """
        repo2 = LanguageWrapper("", Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)

        entry.replaced_tokens["FUNC0@TOKEN@"] = "test1"
        tr = RemoveTokenMarkersTr(context, {})
        entry = repo.parse_code(entry)
        tr.run(entry)
        assert entry.code == r"""
        int test1(){
            int test1, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", test1, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """

    def test_simple2(self):
        code = r"""
        int FUNC0@TOKEN@(){
            int VAR1@TOKEN@, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", VAR1@TOKEN@, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """
        repo2 = LanguageWrapper("", Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)

        entry.replaced_tokens["FUNC0@TOKEN@"] = "test1"
        entry.replaced_tokens["VAR1@TOKEN@"] = "test1"
        tr = RemoveTokenMarkersTr(context, {})
        entry = repo.parse_code(entry)
        tr.run(entry)
        assert entry.code == r"""
        int test1(){
            int test1, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", test1, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """

    def test_simple2_custom_marker_token(self):
        code = r"""
        int FUNC0@TEST_TOKEN@(){
            int VAR1@TEST_TOKEN@, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", VAR1@TEST_TOKEN@, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """
        repo2 = LanguageWrapper("", Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)

        entry.replaced_tokens["FUNC0@TEST_TOKEN@"] = "test1"
        entry.replaced_tokens["VAR1@TEST_TOKEN@"] = "test1"
        tr = RemoveTokenMarkersTr(context, {"MARKER": "@TEST_TOKEN@"})
        entry = repo.parse_code(entry)
        tr.run(entry)
        print(entry.code)
        assert entry.code == r"""
        int test1(){
            int test1, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", test1, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """
