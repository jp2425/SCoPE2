from tree_sitter import Tree

class ProcessingEntry:

    def __init__(self, code:str):
        self._code: str = code
        self._tree:Tree = None
        self.is_tree_updated: bool = False

        self._replaced_tokens = {} #context with a dictionary with all replaced tokens. Example of value: @TOKEN_{0}@ : value
        self._query:str = ""
        self.detection_result = {}
        self._context = {}
        self._transformations_applied = []

    @property
    def transformations_applied(self):
        return self._transformations_applied.copy()

    def add_transformations_applied(self, transformation_name: str):
        """
        THIS FUNCTION SHOULD NOT BE USED BY THE USER. THIS IS DONE AUTOMATICALLY!
        Adds a transformation name to the list of transformations applied.
        :param transformation_name: name of the transformation ran.
        """
        self._transformations_applied.append(transformation_name)

    #@transformations_applied.setter
    #def transformations_applied(self, transformations_applied):
    #    self._transformations_applied = transformations_applied

    def get_transformation_context(self, transformation_name:str):
        try:
            return self._context[transformation_name]
        except:
            return {}

    def update_context(self, context:dict):
        """
        Appends / updates the context of a transformation.
        :param context: context in dictionary to append. It must be in format: {"TRANSFORMATION_NAME": {"KEY": "VALUE, "KEY2": "VALUE", ...}}
        :return:
        """
        #TODO: VALIDATION OF NEW CONTEXT
        self._context.update(context)



    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    @property
    def replaced_tokens(self):
        return self._replaced_tokens

    @replaced_tokens.setter
    def replaced_tokens(self, value):
        self._replaced_tokens = value





    @property
    def tree(self):
        if not self.is_tree_updated:
            raise Exception("The tree is not updated! The source code was updated, but the tree wasn't")
        return self._tree

    @tree.setter
    def tree(self, tree):
        self._tree = tree
        self.is_tree_updated = True

    @property
    def code(self):
        return self._code


    @code.setter
    def code(self, code):
        self._code = code
        self.is_tree_updated = False


