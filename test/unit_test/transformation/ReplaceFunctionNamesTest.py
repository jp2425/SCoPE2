import unittest

import tree_sitter_cpp
from tree_sitter import Language

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.repo.LanguageWrapper import LanguageWrapper
from SCoPE2.repo.RepositoryContext import RepositoryContext
from SCoPE2.repo.implementations.TreeSitterRepo import TreeSitterRepo
from SCoPE2.transformation.implementations.ReplaceFunctionNamesTr import ReplaceFunctionNamesTr


class VariableReplacementTest(unittest.TestCase):
    """
    Test the replacement of variables (transformation)
    """

    yaml_file_content = """
    generalize_functions:
        query: |
              ; Capture IDs and function names with namespaces.
              (function_declarator 
                declarator: [
                ((identifier) @function)
                ( _ name: (identifier) @function)])
        QUERY_ID: function
    """


    def test_simple_replacement(self):
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
        tr = ReplaceFunctionNamesTr(context, repo2.language_file[ReplaceFunctionNamesTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code.replace("\n", ""))
        assert entry.code == r"""
        int FUNC0@TOKEN@(){
            int test1, test2 ,test3 = 0;
            char test_string[] = "hello world!\n";
            printf("%d, %d, %d, %d\n", test1, test2, test3);
            printf("%s\n", test_string);
            return 0;
        }
        """
    def test_simple_replacement2(self):
        code = r"""
        test2(teste1, teste3)(int pivete){ if(teste1 == 10){ teste1 = teste1 + 1; test2(teste1,teste3+teste1);} return teste3; }
        """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceFunctionNamesTr(context, repo2.language_file[ReplaceFunctionNamesTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print("##### ", entry.code.replace("\n", ""))
        assert entry.code == r"""
        FUNC0@TOKEN@(teste1, teste3)(int pivete){ if(teste1 == 10){ teste1 = teste1 + 1; FUNC0@TOKEN@(teste1,teste3+teste1);} return teste3; }
        """
    def test_simple_replacement3(self):
        code = r"""
void FullFramePixelBuffer::setBuffer(int width, int height, rdr::U8 * data_, int stride_) { printf("teste\n")}
    """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceFunctionNamesTr(context, repo2.language_file[ReplaceFunctionNamesTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code.replace("\n", ""))
        assert entry.code == r"""
void FullFramePixelBuffer::FUNC0@TOKEN@(int width, int height, rdr::U8 * data_, int stride_) { printf("teste\n")}
    """
    def test_simple_replacement4(self):
        code = r"""
void LineBitmapRequester::ReconstructRegion(const RectAngle<LONG> &orgregion,const struct RectangleRequest *rr){ printf(\"test!\");}
    """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceFunctionNamesTr(context, repo2.language_file[ReplaceFunctionNamesTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code.replace("\n", ""))
        assert entry.code == r"""
void LineBitmapRequester::FUNC0@TOKEN@(const RectAngle<LONG> &orgregion,const struct RectangleRequest *rr){ printf(\"test!\");}
    """