import unittest

import tree_sitter_cpp
from tree_sitter import Language

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.repo.LanguageWrapper import LanguageWrapper
from SCoPE2.repo.RepositoryContext import RepositoryContext
from SCoPE2.repo.implementations.TreeSitterRepo import TreeSitterRepo
from SCoPE2.transformation.implementations.ReplaceVariableNamesTr import ReplaceVariableNamesTr
from SCoPE2.transformation.renameStrategy.minifyReplacement import MinifyReplacement
from SCoPE2.transformation.renameStrategy.simpleReplacement import SimpleReplacement
import os

class VariableReplacementTest(unittest.TestCase):
    """
    Test the replacement of variables (transformation)
    """

    yaml_file_content = """
    generalize_vars:
        query: |
          ; (init_declarator 
          ; declarator: (identifier) @variable) 
          
          (declaration 
            declarator:  [ 
            (identifier) @variable 
            ( _ (identifier) @variable )  
            ( _ ( _ (identifier) @variable ))
         
           ]
           );  the '_' matches with any node.... https://tree-sitter.github.io/tree-sitter/using-parsers
          
           ; declarator:  [ 
           ; (identifier) @variable 
           ; ( _ ( _ (identifier) @variable )) 
         
           ;]
          
          ;(parameter_declaration  JUNTAR O PARAMETER DECLARATION das funcoes >< ================= remover se for preciso
          (parameter_declaration  
          declarator: [ 
              ( _  (_(identifier)  @variable)) ;qqr um e depois um identificador (apanha os & dos pointers...) 
        
            ( _ (identifier)  @variable) ;qqr um e depois um identificador (apanha os & dos pointers...) 
           (identifier) @variable 
           ]) 
           
          ( optional_parameter_declaration  
          declarator: [ 
              ( _  (_(identifier)  @variable)) ;qqr um e depois um identificador (apanha os & dos pointers...) 
        
            ( _ (identifier)  @variable) ;qqr um e depois um identificador (apanha os & dos pointers...) 
           (identifier) @variable 
           ])
          ;  declarator: [ 
          ; ( _ (identifier)  @variable)
          ; (identifier) @variable 
          ; ]
    
        QUERY_ID: variable
    """
    @classmethod
    def setUpClass(cls):
        os.chdir("../")
        print("Diretorio atual: ", os.getcwd())

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
        repo2 = LanguageWrapper(self.yaml_file_content,Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceVariableNamesTr(context, repo2.language_file[ReplaceVariableNamesTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code.replace("\n",""))
        assert entry.code.replace("\n","") == r"""        int test_simple_replacement(){            int VAR0@TOKEN@, VAR1@TOKEN@ ,VAR2@TOKEN@ = 0;            char VAR3@TOKEN@[] = "hello world!\n";            printf("%d, %d, %d, %d\n", VAR0@TOKEN@, VAR1@TOKEN@, VAR2@TOKEN@);            printf("%s\n", VAR3@TOKEN@);            return 0;        }        """

    def test_simple_replacement_multiple_tokens_same_name(self):

        code = r"""
        int test_simple_replacement(){
            int value = 10; 
            int* valuePtr = &value;

            char test_string[] = "hello world! what a nice value!\n";
            printf("%d, %d\n", value, *value);
            printf("%s\n", test_string);
            return 0;
        }
        """

        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceVariableNamesTr(context, repo2.language_file[ReplaceVariableNamesTr.TRANSFORMATION_NAME])
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        assert entry.code.replace("\n","") == r"""        int test_simple_replacement(){            int VAR0@TOKEN@ = 10;             int* VAR1@TOKEN@ = &VAR0@TOKEN@;            char VAR2@TOKEN@[] = "hello world! what a nice VAR0@TOKEN@!\n";            printf("%d, %d\n", VAR0@TOKEN@, *VAR0@TOKEN@);            printf("%s\n", VAR2@TOKEN@);            return 0;        }        """


    def test_minify_replacement_multiple_tokens_same_name(self):

        code = r"""
        int test_simple_replacement(){
            int value = 10; 
            int* valuePtr = &value;

            char test_string[] = "hello world! what a nice value!\n";
            printf("%d, %d\n", value, *value);
            printf("%s\n", test_string);
            return 0;
        }
        """

        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        v = dict(repo2.language_file[ReplaceVariableNamesTr.TRANSFORMATION_NAME])
        v["rename_strategy"] = MinifyReplacement()
        tr = ReplaceVariableNamesTr(context, v)
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code.replace("\n",""))
        assert entry.code.replace("\n","") == r"""        int test_simple_replacement(){            int a@TOKEN@ = 10;             int* b@TOKEN@ = &a@TOKEN@;            char c@TOKEN@[] = "hello world! what a nice a@TOKEN@!\n";            printf("%d, %d\n", a@TOKEN@, *a@TOKEN@);            printf("%s\n", c@TOKEN@);            return 0;        }        """

    def test_replacement_cpp(self):

        code = r"""void LineBitmapRequester::testfunction(const RectAngle<LONG> &orgregion,const struct RectangleRequest *rr){ printf(\"test!\");}"""

        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        v = dict(repo2.language_file[ReplaceVariableNamesTr.TRANSFORMATION_NAME])
        tr = ReplaceVariableNamesTr(context, v)
        entry = repo.parse_code(entry)
        repo.process_query_result(entry, repo.run_query(entry, tr.query()))
        tr.run(entry)
        print(entry.code+"#")
        assert entry.code == r"""void LineBitmapRequester::testfunction(const RectAngle<LONG> &VAR0@TOKEN@,const struct RectangleRequest *VAR1@TOKEN@){ printf(\"test!\");}"""

