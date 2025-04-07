from dataclasses import dataclass

@dataclass
class ControllerTransformationListDto:
    remove_comments: bool
    save_comments: bool
    generalize_strings: bool
    save_strings: bool
    generalize_functions: bool
    generalize_vars: bool
    replace_equivalent_values: bool
    normalize_spacing: bool
    prettify_code: bool

