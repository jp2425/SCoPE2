# Instalation

To use this library, you first need to install it. To do that, clone this repository and, in the repository directory, run the command:

````commandline
pip install .
````

# Usage

An example of a possible usage of this library is presented bellow:

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

This simple example does:

* `transformations = [RemoveCommentsTr, SaveStringsTr, ReplaceVariableNamesTr, RemoveTokenMarkersTr]`  
First the transformations to be used are defined in an array. Those can be transformations sipped with SCoPE2 or can be custom implementations. **DON'T INITIALIZE THE TRANSFORMATIONS! THIS IS DONE INTERNALLY BY SCOPE!**
* The SCoPE class needs two arguments:
  * The configuration of all transformations used. This should be a string. It can be read from a file.
  * A treesitter language object. In this example it is used the C++ language.
* Finally, the process function is called with the code to be processed, the transformations defined earlier and final representation of source code.  
  This last argument defines how the processed code is represented. By default, SCoPE has implemented two code representations:
  * CodeRepresentation: returns the code as a string
  * TokenRepresentation: returns the code as an array of tokens (useful for some AI applications).


## Extending SCoPE

This library was designed to be highly extensible. The next sections will explain how to add more functionality to SCoPE.


#### Adding new transformations

In this section, a new transformation for a different programming language will be developed.

This transformation will detect for loops and append a comment before the for loop declaration. The code would be something like:

```python
class AddCommentJavaForDeclaration(QueryTransformation):

    TRANSFORMATION_NAME: str = "add_comment_to_for_declaration"
    _PHASE = Phase.PROCESSING
    _DEFAULT_CONFIG = {}

    def __init__(self, repo_context: RepositoryContext, config: dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)
        super().__init__(repo_context, self.TRANSFORMATION_NAME, self._PHASE, self._DEFAULT_CONFIG)
        self._repo = repo_context.tree_sitter_repo

    def run(self, entry: ProcessingEntry) -> ProcessingEntry:

        for_structures = self.detect(entry)
        for struct in for_structures:
            entry.code = entry.code.replace(struct, "//This is a dummy transformation\n"+struct)
        return entry

    def query(self) -> str:
        return self._DEFAULT_CONFIG['query']

    def detect(self, entry: ProcessingEntry) -> list:
        return entry.detection_result[self._DEFAULT_CONFIG['QUERY_ID']]
```

And to use it, a new entry in the configuration would need to be added:

```
add_comment_to_for_declaration:
    query: |
        [
        (for_statement)
        (enhanced_for_statement)
        ] @for_structure
    
    QUERY_ID: for_structure
    
remove_comments:
    query: |
        [
        (line_comment)
        (block_comment)
        ] @comment
    QUERY_ID: comment
```