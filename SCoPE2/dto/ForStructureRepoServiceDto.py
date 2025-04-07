from dataclasses import dataclass
from typing import List

@dataclass
class ForStructureRepoServiceDto:

    def __init__(self, for_structure:str, declaration:str, condition:str, update:str, body: str, var_ids:List[str]):
        self.declaration = declaration
        self.condition = condition
        self.update = update
        self.body = body
        self.var_ids = var_ids
        self.for_structure = for_structure