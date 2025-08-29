#!/usr/bin/env python3
"""
add_missing_close.py - Add the missing closing parenthesis for lib_symbols
"""

import sys

def fix_lib_symbols_closure(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    print("Analyzing the structure...")
    
    # Show current state
    print("\nCurrent lines 1091-1095:")
    for i in range(1090, 1095):
        if i < len(lines):
            print(f"  Line {i+1}: {repr(lines[i].rstrip())}")
    
    # Insert a closing parenthesis at line 1093
    print("\nInserting closing parenthesis at line 1093...")
    
    # Make sure line 1093 is a single closing paren with no indent
    lines[1092] = ')\n'  # This becomes the new line 1093
    lines.insert(1092, '  )\n')  # Keep the original line 1092
    
    print("\nFixed lines 1091-1096:")
    for i in range(1090, 1096):
        if i < len(lines):
            print(f"  Line {i+1}: {repr(lines[i].rstrip())}")
    
    # Write the fixed file
    output_file = filepath + '.fixed2'
    with open(output_file, 'w') as f:
        f.writelines(lines)
    
    print(f"\nFixed file saved as: {output_file}")
    
    # Verify parenthesis balance
    print("\nVerifying parenthesis balance in lib_symbols section...")
    balance = 0
    lib_symbols_found = False
    
    for i, line in enumerate(lines[:1100], 1):
        if '(lib_symbols' in line:
            lib_symbols_found = True
            print(f"  lib_symbols starts at line {i}")
        
        if lib_symbols_found:
            opens = line.count('(')
            closes = line.count(')')
            balance += opens - closes
            
            if i in [1091, 1092, 1093, 1094, 1095]:
                print(f"  Line {i}: opens={opens}, closes={closes}, balance={balance}")
            
            if '(junction' in line:
                if balance == 0:
                    print(f"  ✓ Junction found at line {i} with balance=0 (lib_symbols properly closed)")
                else:
                    print(f"  ✗ Junction found at line {i} with balance={balance} (lib_symbols NOT closed)")
                break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 add_missing_close.py <file>")
        sys.exit(1)
    
    fix_lib_symbols_closure(sys.argv[1])
