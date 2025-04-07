from dataclasses import dataclass
from tree_sitter import Tree

@dataclass
class TransformationDto:
    code:str
    tree:Tree