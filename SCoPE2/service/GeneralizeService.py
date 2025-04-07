from ..dto.GeneralizeDto import GeneralizeDto

class GeneralizeService(object):
    _instance = None

    _blacklist_function = [  # function names that we don't want to generalize (like the main function)
        "main"
    ]

    def __init__(self,  dto: GeneralizeDto):

        self.replacementStrategy = dto.replacement_strategy
        self.generalize_functions = dto.generalize_functions
        self.generalize_vars = dto.generalize_vars
        self.generalize_strings = dto.generalize_strings
        self.generalize_classes = dto.generalize_classes

    def _get_function_name(self):
        """
        Gets the function name to be used in generalization.
        We may have multiple strategies to name functions/variables
        """

        return self.replacementStrategy.get_function_name()

    def _get_variable_name(self):
        """
        Gets the function name to be used in generalization.
        We may have multiple strategies to name functions/variables
        """

        return self.replacementStrategy.get_variable_name()

    def translate_string(self, token):
        """
        Function used to translate strings.
        Returns the string replacer or the token.
        """

        if not self.generalize_strings:
            return token
        if self.generalize_strings:
            return self.replacementStrategy.get_string_replacer()
        return token

    def translateFunction(self, name):
        if not self.generalize_functions or (
                name in self._blacklist_function):  # some function names we may not want to replace
            return name

        self.dictionary[name] = self._get_function_name()
        return self.dictionary[name]  # name
    def sortDict(self):
        test_dict_list = list(self.dictionary.items())
        test_dict_list.sort(key=len,reverse=True)

        # reordering to dictionary
        self.dictionary = {ele[0]: ele[1] for ele in test_dict_list}
        return self.dictionary

    def translateVariable(self, name):
        if not self.generalize_vars or name == self.replacementStrategy.get_string_replacer():  # safeguard against replacement of already generalized strings
            return name

        self.dictionary[name] = self._get_variable_name()

        return self.dictionary[name]#name

    '''def translateClass(self, name):
        if not self.generalize_classes:
            return name
        self.class_counter = self.class_counter + 1
        self.dictionary[name] = self.class_prefix + str(self.class_counter - 1)
        return name  # self.class_prefix+str(self.class_counter-1)'''

    def isGeneralizationEnabled(self):
        return self.generalize_functions or self.generalize_vars or self.generalize_classes or self.generalize_strings

    def translate(self, name):
        """
        Returns the name in the dictionary that matches to a specific token.
        Basically:
          name: hi
          Dictionary: ["hi":"bye", "hello":"gd bye"]
          return: "bye"
        """
        if name in self.dictionary:
            return self.dictionary[name]
        return name