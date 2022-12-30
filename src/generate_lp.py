#!/usr/bin/env python3
import argparse
from Dataset import Dataset


class LPGenerator:
    def __init__(self, dataset : Dataset):
        self.dataset = dataset
        
    def write_lp_to_file(self, outfile):
        self.candidates = dataset.get_candidates()
        
        outfile.write(self._generate_objective())
        for party in self.dataset.get_parties():
            outfile.write(self._generate_party_seats_constraint(party))
            
        for constituency in self.dataset.get_constituencies():
            outfile.write(self._generate_constituency_single_winner_constraint(constituency))
            
        outfile.write(self._generate_declaration())
        
    def _generate_objective(self):
        terms = [self._generate_objective_term(candidate)
                 for candidate in self.dataset.get_candidates()]
        return f"max: {' + '.join(terms)};\n"
    
    def _generate_objective_term(self, candidate):
        return f"{candidate.get_variable_name()} {self.dataset.get_votes_of_candidate(candidate)}"
       
    def _generate_party_seats_constraint(self, party):
        num_seats = self.dataset.get_seats_of_party(party)
        candidate_variables = [candidate.get_variable_name()
                               for candidate in self.dataset.get_party_candidates(party)]
        return f"{' '.join(candidate_variables)} <= {num_seats};\n"
    
    def _generate_constituency_single_winner_constraint(self, constituency):
        candidate_variables = [candidate.get_variable_name()
                               for candidate in self.dataset.get_constituency_candidates(constituency)]
        return f"{' '.join(candidate_variables)} = 1;\n"
    
    def _generate_declaration(self):
        candidate_variables = [candidate.get_variable_name()
                               for candidate in self.dataset.get_candidates()]
        return f"binary {', '.join(candidate_variables)};\n"
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("votes", type=str)
    parser.add_argument("seats", type=str)
    parser.add_argument("lpfile", type=str)
    args = parser.parse_args()
    
    dataset = Dataset(votes_file=args.votes, seats_file=args.seats)
    generator = LPGenerator(dataset)
    with open(args.lpfile, "w") as outfile:
        generator.write_lp_to_file(outfile)
