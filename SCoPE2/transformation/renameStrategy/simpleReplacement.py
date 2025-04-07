from .replacementStrategy import ReplacementStrategy


class SimpleReplacement(ReplacementStrategy):

    def __init__(self):
        self.variable_prefix = "VAR"
        self.function_prefix = "FUNC"
        self.class_prefix = "CLASS"
        self.string_replacer = "STRING_TOKEN"

        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0

    def get_function_name(self):
        self.function_counter = self.function_counter + 1
        return self.function_prefix + str(self.function_counter - 1)

    def get_variable_name(self):
        self.variable_counter = self.variable_counter + 1
        return self.variable_prefix + str(self.variable_counter - 1)

    def get_string_replacer(self):
        return self.string_replacer