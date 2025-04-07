from dataclasses import dataclass

from .ControllerTransformationListDto import ControllerTransformationListDto
from ..transformation.renameStrategy.replacementStrategy import ReplacementStrategy


@dataclass
class ControllerServiceInitDto:
    code: str
    return_type: int
    replace_strategy: ReplacementStrategy
    transformations: ControllerTransformationListDto

