#!/bin/bash
echo -n "enter input without extension: "
read input
pstops '"2:0L@1.0(1w,0)+1L@1.0(1w,0.5h)"' $input.ps output.ps
exit 0
