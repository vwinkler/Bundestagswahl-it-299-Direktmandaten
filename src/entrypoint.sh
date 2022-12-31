#!/bin/sh

echo "Generating linear program.."
./generate_lp.py $1 $2 /tmp/problem.lp
echo "Solving linear program.."
lp_solve /tmp/problem.lp > /tmp/lp_result.txt
echo "Evaluating result.."
./print_result_info.py $1 $2 /tmp/lp_result.txt > $3
echo "Done"
