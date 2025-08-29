#!/usr/bin/env python3
"""
find_extra_paren.py - Find the extra closing parenthesis
"""

import sys

def analyze_full_lib_symbols(filepath):
    """Analyze the entire lib_symbols section to find the mismatch"""
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    print("SEARCHING FOR PARENTHESIS MISMATCH IN LIB_SYMBOLS...\n")
    
    # Find lib_symbols start
    lib_symbols_start = 0
    for i, line in enumerate(lines):
        if '(lib_symbols' in line:
            lib_symbols_start = i + 1
            print(f"lib_symbols starts at line {lib_symbols_start}")
            break
    
    # Track balance through entire lib_symbols
    balance = 0
    expected_balance = 0
    in_lib_symbols = False
    lib_symbols_base_depth = 0
    
    for line_num in range(lib_symbols_start - 1, min(1095, len(lines))):
        line = lines[line_num]
        
        if '(lib_symbols' in line:
            in_lib_symbols = True
            lib_symbols_base_depth = balance + 1
            
        old_balance = balance
        opens = line.count('(')
        closes = line.count(')')
        balance += opens - closes
        
        # Check for specific symbols that are problematic
        if 'symbol "power:' in line:
            print(f"\nLine {line_num + 1}: Found power symbol")
            print(f"  Opens: {opens}, Closes: {closes}")
            print(f"  Balance before: {old_balance}, after: {balance}")
            
        # Look for where balance goes negative (extra close)
        if balance < 0:
            print(f"\n🔴 ERROR at line {line_num + 1}:")
            print(f"  Balance went negative! ({balance})")
            print(f"  Line: {line.strip()}")
            print(f"  This indicates an extra closing parenthesis or missing opening parenthesis earlier")
            
        # Check specific problem lines
        if line_num + 1 in [1091, 1092, 1093, 1094]:
            indent = len(line) - len(line.lstrip())
            print(f"Line {line_num + 1} [indent={indent:2d}]: balance={balance:3d} | {line.strip()[:60]}")
            
        if '(junction' in line:
            print(f"\n⚠️ Junction found at line {line_num + 1}, balance={balance}")
            if balance > 0:
                print(f"  Still {balance} levels deep - lib_symbols NOT closed!")
            break
    
    # Now let's check each symbol definition for balance
    print("\n" + "="*60)
    print("CHECKING EACH SYMBOL DEFINITION:")
    print("="*60)
    
    current_symbol = None
    symbol_balance = 0
    symbol_start_line = 0
    
    for line_num in range(lib_symbols_start - 1, min(1095, len(lines))):
        line = lines[line_num]
        
        # Starting a new symbol definition
        if '(symbol "' in line and 'lib_id' not in line:
            if current_symbol and symbol_balance != 0:
                print(f"⚠️ Symbol '{current_symbol}' has unclosed parens: balance={symbol_balance}")
                
            import re
            match = re.search(r'\(symbol\s+"([^"]+)"', line)
            if match:
                current_symbol = match.group(1)
                symbol_start_line = line_num + 1
                symbol_balance = 0
                print(f"\nSymbol: {current_symbol} (starts at line {symbol_start_line})")
        
        if current_symbol:
            opens = line.count('(')
            closes = line.count(')')
            symbol_balance += opens - closes
            
            # Check if symbol is complete
            if symbol_balance == 0 and opens == 0 and closes > 0:
                print(f"  Closed at line {line_num + 1} ✓")
                current_symbol = None
                
        if '(junction' in line:
            break
            
    return balance

def check_power_gnd_symbol(filepath):
    """Focus specifically on the power:GND symbol"""
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    print("\n" + "="*60)
    print("DETAILED CHECK OF power:GND SYMBOL (lines 1061-1091):")
    print("="*60)
    
    # Check the structure matches expected format
    expected_structure = [
        ('1061', '(symbol "power:GND"', 1),  # Opens symbol
        ('1071', '(symbol "GND_0_1"', 1),    # Opens sub-symbol
        ('1084', ')', -1),                   # Closes sub-symbol  
        ('1085', '(symbol "GND_1_1"', 1),    # Opens sub-symbol
        ('1090', ')', -1),                   # Closes sub-symbol
        ('1091', ')', -1),                   # Closes power:GND
    ]
    
    for exp_line, exp_content, exp_change in expected_structure:
        line_num = int(exp_line) - 1
        if line_num < len(lines):
            line = lines[line_num].strip()
            if exp_content in line or (exp_content == ')' and line == ')'):
                print(f"  Line {exp_line}: ✓ Found expected: {exp_content}")
            else:
                print(f"  Line {exp_line}: ❌ Expected '{exp_content}' but got: {line[:50]}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 find_extra_paren.py <file>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    
    final_balance = analyze_full_lib_symbols(filepath)
    check_power_gnd_symbol(filepath)
    
    print("\n" + "="*60)
    print("DIAGNOSIS:")
    print("="*60)
    
    if final_balance > 0:
        print(f"""
The lib_symbols section is NOT properly closed!
Balance is {final_balance} when junction is encountered.

FIX REQUIRED:
Add {final_balance} closing parenthes{'is' if final_balance == 1 else 'es'} before the junction.

Specifically, the structure should be:
    )     <!-- Line 1091: closes last symbol -->
  )       <!-- Line 1092: closes lib_symbols -->
  
  (junction ...  <!-- Line 1094: now at root level -->
""")
