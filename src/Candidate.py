from dataclasses import dataclass

@dataclass
class Candidate:
    party : str
    constituency : str
    
    def get_variable_name(self) -> str:
        return f"elected_{self.party}_{self.constituency}"
