from abc import ABC, abstractmethod

class ReplacementStrategy(ABC):

    @abstractmethod
    def get_variable_name(self):
        pass

    @abstractmethod
    def get_function_name(self):
        pass

    @abstractmethod
    def get_string_replacer(self):
        pass