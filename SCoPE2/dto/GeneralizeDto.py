from dataclasses import dataclass

from ..transformation.renameStrategy.replacementStrategy import ReplacementStrategy

@dataclass
class GeneralizeDto:
    replacement_strategy: ReplacementStrategy
    generalize_functions:bool
    generalize_vars:bool
    generalize_strings:bool
    generalize_classes:bool