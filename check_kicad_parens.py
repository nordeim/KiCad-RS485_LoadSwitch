#!/usr/bin/env python3
"""
check_kicad_parens.py

Usage:
  python3 check_kicad_parens.py path/to/RS485_LoadSwitch.kicad_sch.new-fixed

This script reports:
 - total open/close paren counts,
 - the line and column where the paren balance first goes negative (extra ')'),
 - whether the (lib_symbols block opens and where it should close (and if it's missing).
"""
import sys
import re

if len(sys.argv) != 2:
    print("Usage: python3 check_kicad_parens.py file.sch")
    sys.exit(2)

path = sys.argv[1]
lib_token_re = re.compile(r'\(\s*lib_symbols\b')
try:
    with open(path, 'r', encoding='utf-8') as f:
        bal = 0
        first_negative = None
        lib_open_line = None
        lib_open_depth = None
        lib_close_line = None
        line_no = 0
        for line in f:
            line_no += 1
            # Find (lib_symbols occurrences
            if lib_open_line is None and lib_token_re.search(line):
                lib_open_line = line_no
                lib_open_depth = bal + 1  # depth after counting the '(' for this token (approx)
            # Scan characters to keep exact column counts
            for col, ch in enumerate(line, start=1):
                if ch == '(':
                    bal += 1
                elif ch == ')':
                    bal -= 1
                if first_negative is None and bal < 0:
                    first_negative = (line_no, col)
            # If lib_symbols has been opened and the depth decreased to lib_open_depth-1,
            # that means the lib_symbols block ended earlier; but easier: if lib_open_depth is not None
            # and bal < lib_open_depth, we've closed the lib_symbols block.
            if lib_open_line is not None and lib_close_line is None and bal < lib_open_depth:
                lib_close_line = line_no
        # EOF reached
except FileNotFoundError:
    print("File not found:", path)
    sys.exit(1)

print("File:", path)
print("Final parentheses balance (open - close):", bal)
if first_negative:
    print("Balance went negative at line {}, column {} (extra ')').".format(*first_negative))
else:
    print("Balance never went negative during the scan.")

if lib_open_line:
    print("Found '(lib_symbols' opening at line", lib_open_line)
    if lib_close_line:
        print("  The lib_symbols block appears to close by line", lib_close_line)
    else:
        print("  WARNING: lib_symbols block did NOT close before EOF. You likely need to add one or more ')' to close it.")
else:
    print("No '(lib_symbols' token found in file.")

if bal != 0:
    print("Overall parentheses are unbalanced by", bal)
    if bal > 0:
        print("  There are", bal, "more '(' than ')'.")
    else:
        print("  There are", -bal, "more ')' than '('.")

if bal == 0 and not first_negative:
    print("Parentheses appear balanced (at character level).")
