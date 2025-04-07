import warnings
from abc import ABC
from typing import List

from SCoPE2.domain.ProcessingEntry import ProcessingEntry
from SCoPE2.transformation.Transformation import Transformation
from SCoPE2.transformation.phases import Phase


class ProcessService(ABC):

    def __init__(self):
        pass

    def run_transformation_in_phase(self, transformations, entry:ProcessingEntry, phase: Phase) -> (ProcessingEntry, List[Transformation]):
        skipped_one = False
        transformations_to_remove = []
        for transformation in transformations:
            if transformation.transformation_phase == phase or (
                    transformation.transformation_phase == Phase.ANY and skipped_one):
                try:
                    entry = transformation.run(entry)
                except Exception as e:
                    warnings.warn(
                        "[!] The transformation " + transformation.TRANSFORMATION_NAME + " raised an error: " + str(e))
                transformations_to_remove.append(transformation)
                skipped_one = False
            else:
                skipped_one = True
        return entry,  list(filter(lambda item: item not in transformations_to_remove, transformations))