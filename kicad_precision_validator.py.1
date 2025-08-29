#!/usr/bin/env python3
"""
kicad_precision_validator.py

A precision validator that tracks exact parenthesis balance within lib_symbols
to find where the structure is broken.

Usage:
  python3 kicad_precision_validator.py RS485_LoadSwitch.kicad_sch
"""

import sys
import re

class PrecisionValidator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []
        
    def load_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        return True
        
    def find_unclosed_sections(self):
        """Track every opening and closing to find mismatches"""
        
        stack = []  # Stack of (element_name, line_num, col_num, indent)
        line_num = 0
        in_lib_symbols = False
        lib_symbols_start = 0
        lib_symbols_depth = 0
        
        # Pattern to match opening elements
        open_pattern = re.compile(r'KATEX_INLINE_OPEN\s*([a-zA-Z_][a-zA-Z0-9_\-:]*)')
        
        for line_num, line in enumerate(self.lines, 1):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith(';'):
                continue
                
            # Track column position
            col = 0
            i = 0
            while i < len(line):
                if line[i] == '(':
                    # Found opening paren
                    # Try to extract the element name
                    match = open_pattern.match(line[i:])
                    if match:
                        elem_name = match.group(1)
                        indent = len(line) - len(line.lstrip())
                        stack.append((elem_name, line_num, col, indent))
                        
                        if elem_name == 'lib_symbols':
                            in_lib_symbols = True
                            lib_symbols_start = line_num
                            lib_symbols_depth = len(stack)
                            print(f"Line {line_num}: Opening lib_symbols (depth={len(stack)})")
                        elif in_lib_symbols and elem_name == 'symbol':
                            print(f"Line {line_num}: Opening symbol '{line.strip()[:50]}' (depth={len(stack)})")
                    else:
                        # Opening paren without clear element name
                        indent = len(line) - len(line.lstrip())
                        stack.append(('?', line_num, col, indent))
                        
                elif line[i] == ')':
                    # Found closing paren
                    if stack:
                        elem = stack.pop()
                        if elem[0] == 'lib_symbols':
                            print(f"Line {line_num}: CLOSING lib_symbols (was opened at line {elem[1]})")
                            in_lib_symbols = False
                        elif in_lib_symbols and elem[0] == 'symbol':
                            # Get symbol name if possible
                            orig_line = self.lines[elem[1]-1] if elem[1] <= len(self.lines) else ""
                            print(f"Line {line_num}: Closing symbol from line {elem[1]}")
                    else:
                        print(f"Line {line_num}: ERROR - Extra closing paren!")
                        
                    # Check if we just closed lib_symbols
                    if in_lib_symbols and stack and len(stack) < lib_symbols_depth:
                        print(f"Line {line_num}: lib_symbols closure detected")
                        in_lib_symbols = False
                        
                col += 1
                i += 1
                
            # Check for junction while still in lib_symbols
            if in_lib_symbols and 'junction' in line:
                print(f"\n🔴 CRITICAL ERROR at line {line_num}:")
                print(f"  Found 'junction' while still inside lib_symbols!")
                print(f"  lib_symbols opened at line {lib_symbols_start}")
                print(f"  Current stack depth: {len(stack)}")
                print(f"  Stack top elements:")
                for elem in stack[-5:]:
                    print(f"    - {elem[0]} at line {elem[1]}")
                return False
                
        # Final check
        if stack:
            print(f"\n⚠️ Unclosed elements at end of file:")
            for elem in stack:
                print(f"  - {elem[0]} opened at line {elem[1]}, column {elem[2]}")
                
        return True
        
    def check_specific_area(self):
        """Focus on the area around line 1061-1095"""
        
        print("\n" + "="*60)
        print("DETAILED ANALYSIS OF LINES 1061-1095:")
        print("="*60)
        
        # Count parentheses in this specific area
        open_count = 0
        close_count = 0
        
        for line_num in range(1060, 1096):  # Lines 1061-1095
            if line_num >= len(self.lines):
                break
                
            line = self.lines[line_num]
            line_opens = line.count('(')
            line_closes = line.count(')')
            open_count += line_opens
            close_count += line_closes
            
            if line_opens or line_closes:
                balance = open_count - close_count
                indent = len(line) - len(line.lstrip())
                print(f"Line {line_num+1:4d} [indent={indent:2d}]: +{line_opens} -{line_closes} (balance={balance:+3d}) {line.strip()[:60]}")
                
        print(f"\nTotal in this section: {open_count} opens, {close_count} closes")
        if open_count != close_count:
            print(f"⚠️ IMBALANCE: {open_count - close_count:+d} unclosed parentheses!")
            
    def analyze_lib_symbols_structure(self):
        """Analyze the entire lib_symbols section"""
        
        print("\n" + "="*60)
        print("LIB_SYMBOLS SECTION ANALYSIS:")
        print("="*60)
        
        in_lib_symbols = False
        lib_start = 0
        depth = 0
        base_depth = 0
        
        for line_num, line in enumerate(self.lines, 1):
            if '(lib_symbols' in line:
                in_lib_symbols = True
                lib_start = line_num
                base_depth = depth + 1
                print(f"lib_symbols starts at line {line_num}")
                
            if in_lib_symbols:
                opens = line.count('(')
                closes = line.count(')')
                depth += opens - closes
                
                # Check if we've closed lib_symbols
                if depth < base_depth:
                    print(f"lib_symbols closes at line {line_num}")
                    in_lib_symbols = False
                    
                # Look for symbol definitions
                if '(symbol "' in line and in_lib_symbols:
                    symbol_match = re.search(r'KATEX_INLINE_OPENsymbol\s+"([^"]+)"', line)
                    if symbol_match:
                        print(f"  Line {line_num}: Symbol '{symbol_match.group(1)}' (depth={depth})")
                        
                # Check for unexpected elements
                if in_lib_symbols:
                    for elem in ['junction', 'wire', 'no_connect']:
                        if f'({elem}' in line:
                            print(f"\n🔴 ERROR: Found '{elem}' at line {line_num} inside lib_symbols!")
                            print(f"  Current depth: {depth}, base depth: {base_depth}")
                            print(f"  This means lib_symbols is NOT closed!")
                            return False
                            
        return True
        
    def suggest_fix(self):
        """Provide specific fix instructions"""
        
        print("\n" + "="*60)
        print("RECOMMENDED FIX:")
        print("="*60)
        
        print("""
Based on the analysis, the lib_symbols section is missing a closing parenthesis.

TO FIX:
1. The last symbol "power:GND" closes at line 1091
2. Line 1092 has a ')' but it's not enough to close lib_symbols
3. You need to ensure lib_symbols is properly closed

VERIFY THE FIX:
After line 1091 which closes the last symbol, you should have:
    )     <!-- Line 1091: closes power:GND symbol -->
  )       <!-- Line 1092: closes lib_symbols (2 spaces indent) -->
  
  (junction (at 50.8 50.8) ...  <!-- Line 1094: Now at root level -->

The key is that line 1092 should have exactly 2 spaces before the ')' to match
the indentation of where lib_symbols opened.
""")
        
    def run(self):
        """Run all validations"""
        print(f"Analyzing: {self.filepath}")
        print("="*60)
        
        if not self.load_file():
            return
            
        # Run all checks
        self.check_specific_area()
        
        if not self.find_unclosed_sections():
            self.suggest_fix()
            
        self.analyze_lib_symbols_structure()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 kicad_precision_validator.py <schematic_file>")
        sys.exit(1)
        
    validator = PrecisionValidator(sys.argv[1])
    validator.run()
