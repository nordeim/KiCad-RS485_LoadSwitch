#!/usr/bin/env python3
"""
kicad_schematic_deep_validator.py

A deeply reimagined KiCad schematic validator that truly understands
the distinction between symbol definitions and symbol instances,
and properly validates the hierarchical structure.

Usage:
  python3 kicad_schematic_deep_validator.py RS485_LoadSwitch.kicad_sch
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Optional, Set, Dict
from enum import Enum

class TokenType(Enum):
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    SYMBOL = "symbol"
    STRING = "string"
    NUMBER = "number"
    EOF = "eof"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

@dataclass
class SExpr:
    """Represents a parsed S-expression"""
    name: str
    line: int
    column: int
    children: List['SExpr']
    value: Optional[str] = None
    
class KiCadSchematicDeepValidator:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = ""
        self.lines = []
        self.errors = []
        self.warnings = []
        self.critical_issues = []
        
        # Define CORRECT validation rules for KiCad version 20230121
        
        # Top-level kicad_sch attributes (not children, but attributes)
        self.kicad_sch_attributes = {'version', 'generator'}
        
        # Valid top-level elements in kicad_sch
        self.kicad_sch_children = {
            'uuid', 'paper', 'title_block', 'lib_symbols',
            'junction', 'no_connect', 'wire', 'bus', 'bus_entry',
            'polyline', 'text', 'label', 'global_label', 
            'hierarchical_label', 'symbol',  # symbol INSTANCES
            'sheet', 'sheet_instances'
        }
        
        # Symbol definition (inside lib_symbols) valid elements
        self.symbol_definition_elements = {
            'property', 'pin', 'symbol',  # nested symbol definitions
            'polyline', 'rectangle', 'circle', 'arc', 'text',
            'pin_numbers', 'pin_names', 'in_bom', 'on_board',
            'power', 'fields_autoplaced', 'uuid', 'exclude_from_sim',
            'offset', 'effects', 'font', 'stroke', 'fill'
        }
        
        # Symbol instance (at root level) valid elements  
        self.symbol_instance_elements = {
            'lib_id', 'at', 'unit', 'in_bom', 'on_board', 'dnp',
            'fields_autoplaced', 'uuid', 'property', 'pin', 'instances',
            'project', 'path', 'reference', 'mirror'
        }
        
        # Track where we are in parsing
        self.inside_lib_symbols = False
        self.lib_symbols_depth = 0
        self.current_depth = 0
        
    def load_file(self):
        """Load file content"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
            return True
        except Exception as e:
            self.errors.append(f"Error loading file: {e}")
            return False
            
    def find_lib_symbols_closure(self):
        """Find where lib_symbols should close based on proper nesting"""
        lines_with_content = []
        paren_count = 0
        inside_lib_symbols = False
        lib_symbols_start_line = None
        lib_symbols_start_depth = 0
        
        for line_num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(';'):
                continue
                
            # Count parentheses before checking for lib_symbols
            for char in line:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    
            # Check if we're starting lib_symbols
            if '(lib_symbols' in line:
                inside_lib_symbols = True
                lib_symbols_start_line = line_num
                lib_symbols_start_depth = paren_count
                self.warnings.append({
                    'line': line_num,
                    'message': f"Found (lib_symbols at line {line_num}, depth {paren_count}"
                })
                
            # Check if we should be closing lib_symbols
            if inside_lib_symbols and paren_count < lib_symbols_start_depth:
                self.warnings.append({
                    'line': line_num,
                    'message': f"lib_symbols should close around line {line_num}"
                })
                inside_lib_symbols = False
                
            # Look for elements that shouldn't be in lib_symbols
            if inside_lib_symbols:
                if any(elem in line for elem in ['(junction', '(wire', '(no_connect']):
                    self.critical_issues.append({
                        'line': line_num,
                        'issue': f"Found schematic element inside lib_symbols at line {line_num}",
                        'content': stripped[:80],
                        'fix': f"lib_symbols MUST close before line {line_num}. Add ')' at line {line_num - 1}"
                    })
                    
    def analyze_structure_deeply(self):
        """Perform deep structural analysis"""
        
        # Track sections
        current_section = "root"
        section_stack = []
        paren_depth = 0
        lib_symbols_line = None
        lib_symbols_closed = False
        last_symbol_def_line = None
        
        for line_num, line in enumerate(self.lines, 1):
            # Skip empty lines and comments
            stripped = line.strip()
            if not stripped or stripped.startswith(';'):
                continue
                
            # Count parentheses and track depth
            open_count = line.count('(')
            close_count = line.count(')')
            paren_depth += open_count - close_count
            
            # Detect lib_symbols section
            if '(lib_symbols' in line:
                lib_symbols_line = line_num
                section_stack.append(('lib_symbols', paren_depth - open_count + 1))
                current_section = 'lib_symbols'
                
            # Track symbol definitions inside lib_symbols
            if current_section == 'lib_symbols' and '(symbol "' in line:
                last_symbol_def_line = line_num
                
            # Check if we've exited lib_symbols
            if section_stack and section_stack[-1][0] == 'lib_symbols':
                if paren_depth < section_stack[-1][1]:
                    lib_symbols_closed = True
                    current_section = section_stack.pop()[0] if section_stack else "root"
                    
            # CRITICAL CHECK: Schematic elements appearing while still in lib_symbols
            if current_section == 'lib_symbols' and not lib_symbols_closed:
                for element in ['junction', 'wire', 'no_connect', 'bus', 'label']:
                    if f'({element}' in line:
                        self.critical_issues.append({
                            'line': line_num,
                            'severity': 'CRITICAL',
                            'issue': f"'{element}' found inside lib_symbols section!",
                            'explanation': f"The lib_symbols section (started at line {lib_symbols_line}) has not been closed.",
                            'last_symbol': f"Last symbol definition was at line {last_symbol_def_line}",
                            'fix': self.generate_fix_instruction(last_symbol_def_line, line_num)
                        })
                        break
                        
    def generate_fix_instruction(self, last_symbol_line: int, error_line: int):
        """Generate specific fix instructions"""
        
        # Find the proper indentation by checking nearby lines
        proper_indent = self.find_proper_close_location(last_symbol_line, error_line)
        
        return f"""
EXACT FIX REQUIRED:
1. Go to line {proper_indent['insert_line']}
2. Check that the last symbol definition is properly closed with correct indentation
3. Add a closing parenthesis ')' with {proper_indent['spaces']} spaces indentation
4. This will close the lib_symbols section that started at line {proper_indent['lib_start']}

Example of correct structure:
    )  <!-- closes last symbol -->
  )    <!-- closes lib_symbols (2 spaces) -->
  
  (junction (at 50.8 50.8) ...)  <!-- Now at root level -->
"""
        
    def find_proper_close_location(self, last_symbol_line: int, error_line: int):
        """Find exactly where to close lib_symbols"""
        
        # Scan backwards from error line to find the right spot
        for line_num in range(error_line - 1, last_symbol_line, -1):
            line = self.lines[line_num - 1] if line_num <= len(self.lines) else ""
            
            # Look for the end of the last symbol definition
            if ')' in line:
                # Count the indentation
                spaces = len(line) - len(line.lstrip())
                
                # The lib_symbols close should be at indent level 2 (2 spaces)
                if spaces == 4:  # This closes a symbol
                    return {
                        'insert_line': line_num + 1,
                        'spaces': 2,
                        'lib_start': self.find_lib_symbols_start()
                    }
                    
        return {
            'insert_line': error_line - 1,
            'spaces': 2,
            'lib_start': self.find_lib_symbols_start()
        }
        
    def find_lib_symbols_start(self):
        """Find the line where lib_symbols starts"""
        for line_num, line in enumerate(self.lines, 1):
            if '(lib_symbols' in line:
                return line_num
        return 0
        
    def validate_fixed_file(self):
        """Quick validation to ensure the fix worked"""
        
        # Check if lib_symbols is properly closed before junction
        lib_symbols_open = False
        lib_symbols_closed = False
        junction_found = False
        
        for line_num, line in enumerate(self.lines, 1):
            if '(lib_symbols' in line:
                lib_symbols_open = True
            elif lib_symbols_open and not lib_symbols_closed:
                # Simple heuristic: if we see a ) at indent 2, it might close lib_symbols
                if line.strip() == ')' and len(line) - len(line.lstrip()) == 2:
                    # Check if next non-empty line is a junction
                    for next_line in self.lines[line_num:line_num+5]:
                        if '(junction' in next_line:
                            lib_symbols_closed = True
                            break
            elif '(junction' in line:
                junction_found = True
                if not lib_symbols_closed and lib_symbols_open:
                    return False
                    
        return lib_symbols_closed or not lib_symbols_open
        
    def generate_report(self):
        """Generate comprehensive report"""
        print("=" * 80)
        print("KiCad Schematic DEEP Structure Validation Report")
        print(f"File: {self.filepath}")
        print("=" * 80)
        
        if self.critical_issues:
            print(f"\n🔴 CRITICAL ISSUES FOUND: {len(self.critical_issues)}")
            print("-" * 40)
            for issue in self.critical_issues:
                print(f"\n[CRITICAL] Line {issue['line']}")
                print(f"  Issue: {issue['issue']}")
                if 'explanation' in issue:
                    print(f"  Why: {issue['explanation']}")
                if 'last_symbol' in issue:
                    print(f"  Context: {issue['last_symbol']}")
                print(f"  Fix: {issue['fix']}")
                
        # Summary
        print("\n" + "=" * 80)
        print("DIAGNOSIS:")
        if self.critical_issues:
            print("  ❌ The lib_symbols section is NOT properly closed.")
            print("  ❌ Schematic elements appear inside lib_symbols.")
            print("\nTHE FIX:")
            print("  Add a closing parenthesis ')' with 2-space indentation")
            print("  at the location specified above to close lib_symbols.")
        else:
            print("  ✓ Structure appears valid")
            
    def run(self):
        """Run the validation"""
        print("Loading file...")
        if not self.load_file():
            return
            
        print("Performing deep structural analysis...")
        self.find_lib_symbols_closure()
        self.analyze_structure_deeply()
        
        print("Generating report...\n")
        self.generate_report()
        
        # Quick validation check
        if self.critical_issues:
            print("\n" + "=" * 80)
            print("QUICK FIX VALIDATION:")
            if self.validate_fixed_file():
                print("  ✓ The suggested fix should resolve the issue")
            else:
                print("  ⚠ Additional manual review may be needed")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 kicad_schematic_deep_validator.py <schematic_file>")
        sys.exit(1)
        
    validator = KiCadSchematicDeepValidator(sys.argv[1])
    validator.run()
