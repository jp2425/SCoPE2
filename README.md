# SCoPE2
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">


An universal framework for source code transformation. 

```python

import tree_sitter_cpp
from tree_sitter import Language
from SCoPE2.SCoPE import SCoPE
from SCoPE2.representations.CodeRepresentation import CodeRepresentation
from SCoPE2.transformation.implementations import RemoveCommentsTr, RemoveTokenMarkersTr,  ReplaceVariableNamesTr, SaveStringsTr

code = r"""
    int main()
    {
        for(int a = 1; a <10; a++){
            for(int b = 1; b<2; b++){
                printf("%d\n", b*a);
            }
        }
    }"""

transformations = [RemoveCommentsTr, SaveStringsTr, ReplaceVariableNamesTr, RemoveTokenMarkersTr]

scope = SCoPE(open(r"SCoPE2/query/cpp.yaml").read(), Language(tree_sitter_cpp.language()))
print(scope.process(code, transformations, CodeRepresentation))
```

This is an improved version from [SCoPE](https://github.com/jp2425/scope), redesigned to be more efficient and easily customizable.

This is the project repository for the paper "Enhancing Large Language Models with Faster Code Preprocessing for Vulnerability Detection".

For more information about SCoPE2, please take a look at the [docs](docs/) folder.
