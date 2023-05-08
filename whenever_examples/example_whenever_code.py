import os

cwd = os.path.dirname(os.path.abspath(__file__))

cwd1 = os.path.join(cwd, "cwd1.txt")
with open(cwd1, "r") as f:
    example_codes = f.read()

# CODE SNIPPETS FROM https://www.dangermouse.net/esoteric/whenever.html
with open("code2.txt") as f:
    example_code2 = f.read()

# CODE SNIPPETS FROM https://www.dangermouse.net/esoteric/whenever.html
with open("code3.txt") as f:
    example_code3 = f.read()