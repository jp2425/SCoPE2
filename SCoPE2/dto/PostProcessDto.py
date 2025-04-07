from dataclasses import dataclass
from typing import List
from ..domain.ProcessingEntry import ProcessingEntry
from ..transformation.Transformation import Transformation

@dataclass
class PostProcessDto:
    entry: ProcessingEntry
    transformations: List[Transformation]
