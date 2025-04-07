config = {
    "language_query_path": r"C:\Users\josep\Documents\SCoPE2\query\cpp.yaml"
}
transformations = {
    "ReplaceVariableNamesTr": {
        "phase":"processing",
        "type": "query",
        "query_id": ["variable"]
    },
    "ReplaceFunctionNamesTr": {
        "phase": "processing",
        "type": "query",
        "query_id": ["function"]

    },
    "RemoveCommentsTr":{
        "phase":"processing",
        "type": "query",
        "query_id": ["comment"]
    },
    "SaveCommentsTr":{
        "phase":"processing",
        "type": "query",
        "query_id": ["comment"]
    },
    "ReplaceStringsTr":{
        "phase":"processing",
        "type": "query",
        "query_id": ["string"]
    },
    "SaveStringsTr":{
        "phase":"processing",
        "type": "query",
        "query_id": ["string"]
    },
    "ReplaceRepetitionStructTr":{
        "phase":"processing",
        "type": "query",
        "query_id": ["for_structure","var_id","condition","update","body"],
        "declarator_id":"var_id",
        "condition_id": "condition",
        "update_id":"update",
        "body_id":"body"
    },
    "ReplaceLiteralsEquivalentValuesTr":{
        "phase":"processing",
        "type": "replacer"
    },
    "NormalizeSpacingTr":{
        "phase":"post-processing",
        "type": "replacer"
    },
    "PrettifyCodeTr":{
        "phase":"post-processing",
        "type":"replacer"
    }

}