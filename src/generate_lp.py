#!/usr/bin/env python3
import argparse
import pandas as pd
import itertools
from Candidate import Candidate
    
class Dataset:
    def __init__(self, votes_file, seats_file):
        self.votes_relation = pd.read_csv(args.votes)
        self.seats_relation = pd.read_csv(args.seats, index_col="party")
        
        self.votes_matrix = self.votes_relation.pivot(index="constituency", columns="party",
                                                      values="votes")
        
    def get_candidates(self):
        parties = self.get_parties()
        constituencies = self.get_constituencies()
        return [Candidate(party=party, constituency=constituency)
                for (party, constituency) in itertools.product(parties, constituencies)]
        
    def get_parties(self):
        return list(self.seats_relation.index)
    
    def get_constituencies(self):
        return list(self.votes_matrix.index)
    
    def get_party_candidates(self, party : str):
        return [candidate for candidate in self.get_candidates() if candidate.party == party]
    
    def get_constituency_candidates(self, constituency : str):
        return [candidate
                for candidate in self.get_candidates() if candidate.constituency == constituency]
        
    def get_votes_of_candidate(self, candidate : Candidate):
        return self.votes_matrix.loc[candidate.constituency, candidate.party]
    
    def get_seats_of_party(self, party : str):
        return self.seats_relation.loc[party, 'seats'] 


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
