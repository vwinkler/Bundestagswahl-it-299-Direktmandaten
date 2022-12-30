#!/usr/bin/env python3
import argparse
import pandas as pd
import itertools

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("votes", type=str)
    parser.add_argument("seats", type=str)
    parser.add_argument("lpfile", type=str)
    args = parser.parse_args()
    
    votes_relation = pd.read_csv(args.votes)
    seats_relation = pd.read_csv(args.seats, index_col="party")
    
    votes_matrix = votes_relation.pivot(index="constituency", columns="party", values="votes")
    
    parties = seats_relation.index
    constituencies = votes_matrix.index

    with open(args.lpfile, "w") as outfile:
        candidates = list(itertools.product(parties, constituencies))
        elected_candidates = [f"elected_{party}_{constituency} {votes_matrix.loc[constituency, party]}" for (party, constituency) in candidates]
        outfile.write(f"max: {' + '.join(elected_candidates)};\n")
        
        for party in parties:
            elected_candidates = [f"elected_{party}_{constituency}" for constituency in constituencies]
            outfile.write(f"{' '.join(elected_candidates)} <= {seats_relation.loc[party, 'seats']};\n")
            
        for constituency in constituencies:
            elected_candidates = [f"elected_{party}_{constituency}" for party in parties]
            outfile.write(f"{' '.join(elected_candidates)} = 1;\n")
            
        elected_candidates = [f"elected_{party}_{constituency}" for (party, constituency) in candidates]
        outfile.write(f"binary {', '.join(elected_candidates)};")
