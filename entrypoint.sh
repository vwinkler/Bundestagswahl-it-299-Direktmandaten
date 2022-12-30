#!/bin/sh

generate_lp $1 $2 /tmp/problem.lp
lp_solve /tmp/problem.lp > $3
