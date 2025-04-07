import unittest

import tree_sitter_cpp
from tree_sitter import Language

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.repo.LanguageWrapper import LanguageWrapper
from SCoPE2.repo.RepositoryContext import RepositoryContext
from SCoPE2.repo.implementations.TreeSitterRepo import TreeSitterRepo
from SCoPE2.transformation.implementations.ReplaceLiteralsEquivalentValuesTr import ReplaceLiteralsEquivalentValuesTr
from SCoPE2.transformation.renameStrategy.simpleReplacement import SimpleReplacement
import os

class ReplaceLiteralsEquivalentValuesTest(unittest.TestCase):
    yaml_file_content = """
       replace_equivalent_values:
          literals:
              "true": 1 == 1
              "false": 1 == 2
       """
    def test_1(self):
        code = r"""bool isPositive(int number) {
        if (number > 0) {
            return true;
        } else {
            return false;
        }
    }
         """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceLiteralsEquivalentValuesTr(context, repo2.language_file[ReplaceLiteralsEquivalentValuesTr.TRANSFORMATION_NAME])


        entry = tr.run(entry)
        assert entry.code.replace("\n","") == "bool isPositive(int number) {        if (number > 0) {            return 1 == 1;        } else {            return 1 == 2;        }    }         "


    def test_2(self):
        code = r"""bool isLeapYear(int year) {
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
        return true;
    } else {
        return false;
    }
}
         """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceLiteralsEquivalentValuesTr(context, repo2.language_file[
        ReplaceLiteralsEquivalentValuesTr.TRANSFORMATION_NAME])

        entry = tr.run(entry)
        assert entry.code == r"""bool isLeapYear(int year) {
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
        return 1 == 1;
    } else {
        return 1 == 2;
    }
}
         """


    def test_3(self):
        code = r"""bool isEmptyString(const std::string &str) {
    if (str.empty()) {
        return true;
    } else {
        return false;
    }
}
         """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceLiteralsEquivalentValuesTr(context, repo2.language_file[
        ReplaceLiteralsEquivalentValuesTr.TRANSFORMATION_NAME])
        entry = tr.run(entry)
        assert entry.code == r"""bool isEmptyString(const std::string &str) {
    if (str.empty()) {
        return 1 == 1;
    } else {
        return 1 == 2;
    }
}
         """

    def test_4(self):
        code = r"""bool isEmptyString(const std::string &str) {
    if (str.empty()) {
        return true;
    } else {
        return false;
    }
}
         """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        tr = ReplaceLiteralsEquivalentValuesTr(context, repo2.language_file[
            ReplaceLiteralsEquivalentValuesTr.TRANSFORMATION_NAME])
        entry = tr.run(entry)
        assert entry.code == r"""bool isEmptyString(const std::string &str) {
    if (str.empty()) {
        return 1 == 1;
    } else {
        return 1 == 2;
    }
}
         """

    def test_5(self):
        code = r"""bool areEqual(int a, int b) {
    if (a == b) {
        return true;
    } else {
        return false;
    }
}
         """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        v = dict(repo2.language_file[ReplaceLiteralsEquivalentValuesTr.TRANSFORMATION_NAME])
        v.update({"literals": {"true": "1 == 1", "false": "1 == 3"}})
        tr = ReplaceLiteralsEquivalentValuesTr(context, v)
        entry = tr.run(entry)
        assert entry.code == r"""bool areEqual(int a, int b) {
    if (a == b) {
        return 1 == 1;
    } else {
        return 1 == 3;
    }
}
         """

    def test_6(self):
        code = r"""bool isPrime(int number) {
    if (number <= 1) {
        return false;
    }
    for (int i = 2; i <= number / 2; i++) {
        if (number % i == 0) {
            return false;
        }
    }
    return true;
}
         """
        repo2 = LanguageWrapper(self.yaml_file_content, Language(tree_sitter_cpp.language()))
        repo = TreeSitterRepo(repo2)
        context = RepositoryContext(repo)
        entry = ProcessingEntry(code)
        v = dict(repo2.language_file[ReplaceLiteralsEquivalentValuesTr.TRANSFORMATION_NAME])
        v.update({"literals":{"true": "1 == 1","false": "1 == 3"}})
        tr = ReplaceLiteralsEquivalentValuesTr(context, v)
        entry = tr.run(entry)
        assert entry.code == r"""bool isPrime(int number) {
    if (number <= 1) {
        return 1 == 3;
    }
    for (int i = 2; i <= number / 2; i++) {
        if (number % i == 0) {
            return 1 == 3;
        }
    }
    return 1 == 1;
}
         """
