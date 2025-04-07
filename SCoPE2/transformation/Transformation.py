from abc import ABC, abstractmethod
from functools import wraps
from ..domain.ProcessingEntry import ProcessingEntry
from ..exception.InvalidValueException import InvalidValueException
from ..transformation.phases import Phase


class Transformation(ABC):

    def __init__(self, transformation_name: str, transformation_phase: Phase, optional_settings: dict | None) -> None:
        """

        :param transformation_name: the name of the transformation. It must be used in the code when we want to reference the transformation.
                                    For example, one dto may have the variable name "transformationX". This may match with one transformation name, so it is possible to reference the transformation dynamically.
        """
        super().__init__()
        if transformation_name is None or transformation_name == "":
            raise InvalidValueException("The transformation must have a name!")
        self.TRANSFORMATION_NAME = transformation_name

        if transformation_phase is None:
            raise InvalidValueException("The transformation phase is invalid")
        self._TRANSFORMATION_PHASE = transformation_phase
        self._SETTINGS = optional_settings

    @property
    def transformation_phase(self) -> Phase:
        return self._TRANSFORMATION_PHASE

    @property
    def transformation_name(self) -> str:
        return self.TRANSFORMATION_NAME

    @property
    def settings(self):
        return self._SETTINGS

    @staticmethod
    def pre_run_decorator(method):
        """ Decorator for run method """

        @wraps(method)
        def wrapper(self, entry: ProcessingEntry, *args, **kwargs):
            entry.add_transformations_applied(
                self.TRANSFORMATION_NAME)  # Add the transformation name to the context
            return method(self, entry, *args, **kwargs)  # calls the programmer implementation

        return wrapper

    def __init_subclass__(cls, **kwargs):
        """ Ensures all subclasses have the method run decorated automatically """
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "run"):
            cls.run = cls.pre_run_decorator(cls.run)

    @abstractmethod
    def run(self, entry: ProcessingEntry) -> ProcessingEntry:
        '''
        This method will implement the logic of the transformation
        :return:
        '''
        pass
