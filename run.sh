#!/usr/bin/env fish

python3 -m venv .venv

source venv/bin/activate.fish

set dirin "Entradas/EUC_2D/"

set dirout "Saidas/"

set diratt "Entradas/att48.tsp"

# time -v python3 Main.py "$dirin" "$dirout"

# python3 Main.py "$dirin" "$dirout"
for file in "$dirin"/*
	time -v python3 Main.py "$file" "$dirout"
end

