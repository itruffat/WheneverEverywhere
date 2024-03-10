import os

cwd = os.path.dirname(os.path.abspath(__file__))

generic_path = os.path.join(cwd, "code{}.txt")

with open(generic_path.format("1"), "r") as f:
    example_codes = f.read()

# CODE SNIPPETS FROM https://www.dangermouse.net/esoteric/whenever.html
with open(generic_path.format("2"), "r") as f:
    example_code2 = f.read()

# CODE SNIPPETS FROM https://www.dangermouse.net/esoteric/whenever.html
with open(generic_path.format("3"), "r") as f:
    example_code3 = f.read()
