from dataclasses import dataclass
from typing import List

from ..domain.ProcessingEntry import ProcessingEntry
from ..transformation.Transformation import Transformation


@dataclass
class ProcessingDto:
    entry: ProcessingEntry
    transformations: List[Transformation]