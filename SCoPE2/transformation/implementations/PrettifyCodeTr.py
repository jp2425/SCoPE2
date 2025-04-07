from ..phases import Phase
from ...domain.ProcessingEntry import ProcessingEntry
from ...repo.LanguageWrapper import LanguageWrapper
from ..RegularTransformation import RegularTransformation
import re

class PrettifyCodeTr(RegularTransformation):

    TRANSFORMATION_NAME: str = "prettify_code"
    _DEFAULT_CONFIG = {}
    PHASE = Phase.PRE_PROCESSING
    def __init__(self, lang_repo: LanguageWrapper,config:dict, **kwargs):
        self._DEFAULT_CONFIG.update(config)
        super().__init__(lang_repo, self.TRANSFORMATION_NAME, self.PHASE,self._DEFAULT_CONFIG)

    def run(self, entry:ProcessingEntry) -> ProcessingEntry:
        # Expressão regular para capturar strings literais (simples e duplas)
        string_pattern = r'".*?"|\'.*?\''

        # Encontrar todas as strings literais
        strings = re.findall(string_pattern, entry.code)

        # Substituir as strings literais por marcadores temporários
        temp_code = re.sub(string_pattern, "__STRING__", entry.code)

        # Expressão regular para capturar loops for
        for_pattern = r'for\s*\(.*?\)'

        # Encontrar todos os loops for
        fors = re.findall(for_pattern, temp_code)

        # Substituir temporariamente os loops for por marcadores
        temp_code = re.sub(for_pattern, "__FOR_LOOP__", temp_code)

        # Expressão regular para capturar diretivas de pré-processador, como #include, #define, etc.
        header_pattern = r'(?:^|;)\s*#.*\n'

        # Encontrar todas as diretivas de pré-processador
        headers = re.findall(header_pattern, temp_code, re.MULTILINE)

        # Substituir temporariamente as diretivas de pré-processador por marcadores
        temp_code = re.sub(header_pattern, "__HEADER__", temp_code)

        # Remover espaços extras e aplicar formatação ao código (exceto em strings, loops for e headers)
        temp_code = ' '.join(temp_code.split()).replace("\n", "").replace("\t", "")
        temp_code = temp_code.replace(";", ";\n").replace("}", "}\n").replace("{", "{\n")

        spacing = 0
        code_formatted = ""

        # indentar código
        for line in temp_code.splitlines():
            if len(line.strip()) > 0 and line.strip()[-1] == "}":
                spacing -= 4
            line = (" " * spacing) + line.strip()
            if len(line.strip()) > 0 and line.strip()[-1] == "{":
                spacing += 4
            code_formatted = code_formatted + line + "\n"

        # Recolocar os loops for nos lugares originais
        for loop in fors:
            code_formatted = code_formatted.replace("__FOR_LOOP__", loop, 1)

        # Recolocar as strings literais nos lugares originais
        for string in strings:
            code_formatted = code_formatted.replace("__STRING__", string, 1)

        # Recolocar as diretivas de pré-processador nos lugares originais
        for header in headers:
            code_formatted = code_formatted.replace("__HEADER__", header, 1)

        entry.code = code_formatted
        return entry
