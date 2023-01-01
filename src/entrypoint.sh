#!/bin/sh

echo "Converting kerg2 file.."
./convert_kerg2.py $1 /tmp/votes.csv
echo "Generating linear program.."
./generate_lp.py /tmp/votes.csv $2 /tmp/problem.lp
echo "Solving linear program.."
lp_solve /tmp/problem.lp > /tmp/lp_result.txt
echo "Evaluating result.."
./print_result_info.py /tmp/votes.csv $2 /tmp/lp_result.txt > $3
echo "Done"
