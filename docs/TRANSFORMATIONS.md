# Transformations

By default, the SCoPE2 implementation is shipped with some transformations.

### Comments Transformations

These transformations manipulate comments.
  * The [SaveCommentsTr.py](SCoPE2/transformation/implementations/SaveCommentsTr.py) saves comments so they are not modified by mistake by other transformations. 
  * The [RemoveCommentsTr.py](SCoPE2/transformation/implementations/RemoveCommentsTr.py) removes all comments.


### Replacement Transformations


#### Replace for structures with while
The [ReplaceForWithWhileTr.py](SCoPE2/transformation/implementations/ReplaceForWithWhileTr.py) replaces for conditional structures with while structures. Since the code is modified, further transformations  may need to the need of re-parse the code.  
The configuration needed for this transformation is:
* QUERY_ID: The ids of the code elements that are captured by treesitter and used in this transformation. The IDs are separated by commas.

The default values are: 
* QUERY_ID: for_initializer,for_condition,for_update,for_body,for_statement

And since this is a transformation that requires data from treesitter, the default query (for C/C++) is:

```
(for_statement
      initializer: (_) @for_initializer
      condition: (_) @for_condition
      update: (_) @for_update
      body: (_) @for_body
    ) @for_statement
```

For the dummy code bellow, the values obtained from treesitter associated with each "QUERY_ID" are:

```c++
for (int n = 0; n <10; n++){
	int a = n + 1;
   }
```

* for_initializer: "int n = 0;"
* for_condition: "n <10"
* for_update: "n++"
* for_body:"int a = n + 1;
   }"
* for_statement: 
for (int n = 0; n <10; n++){
	int a = n + 1;
   }


#### Replace function names

The [ReplaceFunctionNamesTr.py](SCoPE2/transformation/implementations/ReplaceFunctionNamesTr.py) replaces function names with generic ones. When a function name is detected, it replaces with a dummy code, like FUNC0@TOKEN@. The `@TOKEN@` is used to avoid further modification of the name by other transformations. As such, when this transformation is used it needs to be proceeded by the usage of the `RemoveTokenMarkersTr` transformation to remove the `@TOKEN@`.

The configuration needed for this transformation is:

* QUERY_ID: The id of the code elements that are captured by treesitter and used in this transformation. Default: `function`
* rename_strategy: The strategy used to rename vars. This is an object of a class that implements the ReplacementStrategy abstract class. By default, the `SimpleReplacement` strategy is used, that replaces the variable / function names by sequential generic ones (FUNC0, FUNC1, ...).   
  Other strategy shipped in SCoPE2 is the `MinifyReplacement`, that tries to minify the variable / function names.

The default (C/C++) query used for this transformation is:

```
; Capture IDs and function names with namespaces.
      (function_declarator 
          declarator: [
          ((identifier) @function)
          ( _ name: (identifier) @function)])
```

#### Replace variable names

The [ReplaceVariableNamesTr.py](SCoPE2/transformation/implementations/ReplaceVariableNamesTr.py) replaces variable names with generic ones. When a variable name is detected, it replaces with a dummy code, like VAR0@TOKEN@. The `@TOKEN@` is used to avoid further modification of the name by other transformations. As such, when this transformation is used it needs to be proceeded by the usage of the `RemoveTokenMarkersTr` transformation to remove the `@TOKEN@`.  
Unlike the `ReplaceFunctionNamesTr` transformation, this can operate in 2 modes: it can replace the variable with the `GENERIC@TOKEN@` combination or it can directly replace the variable name with the generic token (like `VAR0`), removing the need to use other transformation to remove the `@TOKEN@`.

The configuration needed for this transformation is:

* QUERY_ID: The id of the code elements that are captured by treesitter and used in this transformation. Default: `variable`.
* rename_strategy: The strategy used to rename vars. This is an object of a class that implements the ReplacementStrategy abstract class. By default, the `SimpleReplacement` strategy is used, that replaces the variable / function names by sequential generic ones (FUNC0, FUNC1, ...).   
  Other strategy shipped in SCoPE2 is the `MinifyReplacement`, that tries to minify the variable / function names.
* safe: selects the mode of operation. When is `False`, it does not add the `@TOKEN@` token to the replaced variable name. Default: `True`.

The default (C/C++) query used for this transformation is:

```

      (declaration 
        declarator:  [ 
        (identifier) @variable 
        ( _ (identifier) @variable )  
        ( _ ( _ (identifier) @variable ))
     
       ]
       );  the '_' matches with any node.... https://tree-sitter.github.io/tree-sitter/using-parsers
      

      (parameter_declaration  
      declarator: [ 
          ( _  (_(identifier)  @variable)) 
    
        ( _ (identifier)  @variable)
       (identifier) @variable 
       ]) 
       
      ( optional_parameter_declaration  
      declarator: [ 
          ( _  (_(identifier)  @variable))
    
        ( _ (identifier)  @variable) 
       (identifier) @variable 
       ])


```

#### Replace literals with equivalent values

The [ReplaceLiteralsEquivalentValuesTr.py](SCoPE2/transformation/implementations/ReplaceLiteralsEquivalentValuesTr.py) replaces literals, like `true` or `false` with equivalent values.

The configuration needed for this transformation is:
* literals: A dictionary with the literal to be replaced : literal to replace (Default: `{"true":"1==1", "false": "1==2"}`)

#### Replace strings 

The [ReplaceStringsTr.py](SCoPE2/transformation/implementations/ReplaceStringsTr.py) transformation replaces strings with a generic token.
The replacement is defined by the ReplacementStrategy (same object type as variable and function replacement)
The configuration needed for this transformation is:

* QUERY_ID: The id of the code elements that are captured by treesitter and used in this transformation. Default: `string`.
* rename_strategy: The replacement strategy. (Default: `SimpleReplacement()`

The default (C/C++) query used for this transformation is:

```
(string_literal) @string
```


### Misc Transformations

* [RemoveTokenMarkersTr.py](../SCoPE2/transformation/implementations/RemoveTokenMarkersTr.py)  
Receives as option the marker to be replaced. By default is `@TOKEN@` (config example: "MARKER": "@TOKEN@")  
It also iterates through the entry.replaced_tokens dictionary. If your transformation wants to have tokens to be replaced at certain point (like at the end), they can add to this dictionary those tokens and the respective value to replace them.  
* [SwapOperatorsTr.py](../SCoPE2/transformation/implementations/SwapOperatorsTr.py)  
Swap code operators.
Default config:  

* QUERY_ID: The id of the code elements that are captured by treesitter and used in this transformation. Default: `swap_expressions`
* SUPPORTED_OPERATORS: has the supported operators. Currently, only those are supported by the transformation: `["<", ">", "<=",">="]`

The default query used in this transformation is:

```
(binary_expression
      operator: [ "<" ">" "<=" ">=" ]
    ) @swap_expressions

```