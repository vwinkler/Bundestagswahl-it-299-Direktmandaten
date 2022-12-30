from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Candidate:
    party : str
    constituency : str
    
    def get_variable_name(self) -> str:
        return f"elected__{self.party}__{self.constituency}"
    
    @staticmethod
    def from_variable_name(variable_name):
        [_, party, constituency] = variable_name.split("__")
        return Candidate(party, constituency)
