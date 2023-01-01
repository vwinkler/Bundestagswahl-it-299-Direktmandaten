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
        feasible = True
        for line in result_file:
            if section == "before variable assignment":
                if re.fullmatch(r"^Actual values of the variables:\s*$", line):
                    section = "variable assignment"
                elif re.fullmatch(r"^This problem is infeasible\s*$", line):
                    feasible = False
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
    if not feasible:
        print("Could not find a seat assignment.")
        print("lp_solve reports this problem to be infeasible.")
        print("Do the number of constituencies and the total number of seats match?")
        exit(1)
            
    dataset = Dataset(votes_file=args.votes, seats_file=args.seats)
            
    for winner in sorted(elected_candidates, key=lambda c: c.constituency):
        print(f"Constituency '{winner.constituency}':")
        print(f"  Elected party: {winner.party}")
        total_votes = dataset.get_num_voters_in_constituency(winner.constituency)
        candidates = dataset.get_constituency_candidates(winner.constituency)
        candidate_votes = [(candidate, dataset.get_votes_of_candidate(candidate))
                           for candidate in candidates]
        candidates_by_votes = sorted(candidate_votes, key=lambda cv: cv[1], reverse=True)
        for (rank, (candidate, votes)) in enumerate(candidates_by_votes):
            print(f"  {rank + 1}. {candidate.party}: {votes} ({votes / total_votes:.2%})")
        print()
    print()
        
    num_constituencies = dataset.get_num_constituencies()
    for party in dataset.get_parties():
        print(f"Party '{party}':")
        elected_party_candidates = [c for c in elected_candidates if c.party == party]
        print(f"  Won constituencies: {len(elected_party_candidates)}/{num_constituencies}"
              f" ({len(elected_party_candidates) / num_constituencies:.2%})")
        constituencies_headed_by_party = dataset.get_num_constituencies_headed_by_party(party)
        print("  Won constituencies had this been a majority election:"
              f" {constituencies_headed_by_party}/{num_constituencies}"
              f" ({constituencies_headed_by_party / num_constituencies:.2%})")
        print()
    print()

    print("All constituencies:")
    num_represented_votes = sum([dataset.get_votes_of_candidate(candidate)
                                 for candidate in elected_candidates])
    print(f"  Number of constituencies: {len(dataset.get_constituencies())}")
    print(f"  Number of parties: {len(dataset.get_parties())}")
    print(f"  Total number of seats: {dataset.get_total_seats()}")
    print(f"  Represented votes: {num_represented_votes}/{dataset.get_num_voters()}"
          f" ({num_represented_votes / dataset.get_num_voters():.2%})")
    print("  Represented votes had this been a majority election:"
          f" {dataset.get_num_constituency_majority_voters()}/{dataset.get_num_voters()}"
          f" ({dataset.get_num_constituency_majority_voters() / dataset.get_num_voters():.2%})")
          
