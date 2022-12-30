#!/usr/bin/env python3
import argparse
import re
from Candidate import Candidate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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
            
    for candidate in sorted(elected_candidates, key=lambda c: c.constituency):
        print(f"Constituency '{candidate.constituency}':")
        print(f"  Elected party: {candidate.party}")
        print()
