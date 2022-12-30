#!/usr/bin/env python3
import argparse
import re
from Candidate import Candidate
from Dataset import Dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("votes", type=str)
    parser.add_argument("seats", type=str)
    parser.add_argument("lp_solve_result_file", type=str)
    args = parser.parse_args()
    
    elected_candidates = set()
    with open(args.lp_solve_result_file) as result_file:
        section = "before variable assignment"
        for line in result_file:
            if section == "before variable assignment":
                if re.fullmatch(r"^Actual values of the variables:\s*$", line):
                    section = "variable assignment"
            elif section == "variable assignment":
                match = re.fullmatch(r"^(\S+)\s+(0|1)\s*$", line)
                if match:
                    if match.group(2) == "1":
                        elected_candidates.add(Candidate.from_variable_name(match.group(1)))
                    else:
                        pass
                else:
                    section = "after variable assignment"
            elif section == "after variable assignment":
                pass
            
    dataset = Dataset(votes_file=args.votes, seats_file=args.seats)
            
    for winner in sorted(elected_candidates, key=lambda c: c.constituency):
        print(f"Constituency '{winner.constituency}':")
        print(f"  Elected party: {winner.party}")
        total_votes = dataset.get_num_voters_in_constituency(winner.constituency)
        candidates = dataset.get_constituency_candidates(winner.constituency)
        candidate_votes = [(candidate, dataset.get_votes_of_candidate(candidate))
                           for candidate in candidates]
        for (candidate, votes) in sorted(candidate_votes, key=lambda cv: cv[1], reverse=True):
            print(f"  {candidate.party}: {votes} ({votes / total_votes:.2%})")
        print()
