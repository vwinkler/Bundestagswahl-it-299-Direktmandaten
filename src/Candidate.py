from dataclasses import dataclass
import re

class NameMangler:
    def __init__(self):
        self.replacements = [
                (" ", "_^"),
                ("__", "$"),
                ("ä", "a^"),
                ("Ä", "A^"),
                ("ö", "o^"),
                ("Ö", "O^"),
                ("ü", "u^"),
                ("Ü", "U^"),
                ("ß", "s^"),
                ("ẞ", "S^"),
                ("³", "3^"),
                ("-", "#"),
                ("–", "~"),
                ("(", "["),
                (")", "]")]
        
    def mangle(self, string : str):
        result = string
        for (old, new) in self.replacements:
            result = result.replace(old, new)
        
        if not re.fullmatch(r"[a-zA-Z_\[\]{}/.&#$%~'@\^][a-zA-Z0-9_\[\]{}/.&#$%~'@\^]*", result):
            print(f"Name '{string}' (represented as '{result}') is not allowed")
        return result
    
    def unmangle(self, string : str):
        result = string
        for (new, old) in self.replacements:
            result = result.replace(old, new)
        return result

@dataclass(eq=True, frozen=True)
class Candidate:
    party : str
    constituency : str
    _mangler = NameMangler()
    
    def get_variable_name(self) -> str:
        return f"elected__{self._mangler.mangle(self.party)}__{self._mangler.mangle(self.constituency)}"
    
    @staticmethod
    def from_variable_name(variable_name):
        [_, party, constituency] = variable_name.split("__")
        return Candidate(Candidate._mangler.unmangle(party), Candidate._mangler.unmangle(constituency))
