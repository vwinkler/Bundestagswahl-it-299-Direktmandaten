import pandas as pd
import itertools
from Candidate import Candidate
    
class Dataset:
    def __init__(self, votes_file, seats_file):
        self.votes_relation = pd.read_csv(votes_file)
        self.seats_relation = pd.read_csv(seats_file, index_col="party")
        
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
    
    def get_num_voters_in_constituency(self, constituency : str):
        return self.votes_matrix.loc[constituency, :].sum()
    
    def get_num_voters(self):
        return self.votes_matrix.values.sum()
    
    def get_seats_of_party(self, party : str):
        return self.seats_relation.loc[party, 'seats']
    
    def get_num_constituency_majority_voters(self):
        return self.votes_matrix.max(axis=1).sum()
