#!/usr/bin/gawk -f
/Merge *pull *request *#[0-9]+/ { print substr($4, 2); exit}
match($0, /\(#[0-9]+\)/) { print substr($0, RSTART+2, RLENGTH-3)}
