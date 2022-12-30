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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("votes", type=str)
    parser.add_argument("seats", type=str)
    parser.add_argument("lpfile", type=str)
    args = parser.parse_args()
    
    dataset = Dataset(votes_file=args.votes, seats_file=args.seats)
    candidates = dataset.get_candidates()
    with open(args.lpfile, "w") as outfile:
        elected_candidates = [f"{candidate.get_variable_name()} {dataset.get_votes_of_candidate(candidate)}"
                              for candidate in candidates]
        outfile.write(f"max: {' + '.join(elected_candidates)};\n")
        
        for party in dataset.get_parties():
            num_seats = dataset.get_seats_of_party(party)
            candidates = dataset.get_party_candidates(party)
            candidate_variables = [candidate.get_variable_name() for candidate in candidates]
            outfile.write(f"{' '.join(candidate_variables)} <= {num_seats};\n")
            
        for constituency in dataset.get_constituencies():
            candidates = dataset.get_constituency_candidates(constituency)
            candidate_variables = [candidate.get_variable_name() for candidate in candidates]
            outfile.write(f"{' '.join(candidate_variables)} = 1;\n")
            
        candidate_variables = [candidate.get_variable_name()
                               for candidate in dataset.get_candidates()]
        outfile.write(f"binary {', '.join(candidate_variables)};")
