#!/bin/bash

echo "=== QUICK ANTLR4 VERSION TEST ==="
echo "1. Command line antlr4:"
which antlr4 && antlr4 --version 2>/dev/null || echo "antlr4 command not found"
echo ""
echo "2. Python antlr4 package:"
python -c "import antlr4; print(f'antlr4 Python package: {antlr4.__file__}')" 2>/dev/null || echo "antlr4 Python package not found"
echo ""
echo "3. Pip package info:"
pip show antlr4-python3-runtime 2>/dev/null | grep -E "(Version|Location)" || echo "antlr4-python3-runtime not found"
echo ""
echo "4. All antlr4 related packages:"
pip list | grep -i antlr || echo "No antlr4 packages found" 