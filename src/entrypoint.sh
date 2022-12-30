#!/bin/sh

./generate_lp.py $1 $2 /tmp/problem.lp
lp_solve /tmp/problem.lp > $3
