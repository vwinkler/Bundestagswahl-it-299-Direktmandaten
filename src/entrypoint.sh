#!/bin/sh

./generate_lp.py $1 $2 /tmp/problem.lp
lp_solve /tmp/problem.lp > /tmp/lp_result.txt
./print_result_info.py /tmp/lp_result.txt > $3
