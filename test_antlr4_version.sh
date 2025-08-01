#!/bin/bash

echo "=== ANTLR4 VERSION TEST ==="
echo ""

# Test 1: Check if antlr4 command exists
echo "1. Testing antlr4 command availability:"
if command -v antlr4 &> /dev/null; then
    echo "✓ antlr4 command found"
    antlr4 --version
else
    echo "✗ antlr4 command not found in PATH"
fi
echo ""

# Test 2: Check Python antlr4 package
echo "2. Testing Python antlr4 package:"
python -c "
try:
    import antlr4
    print('✓ antlr4 Python package imported successfully')
    print(f'antlr4 package location: {antlr4.__file__}')
except ImportError as e:
    print(f'✗ antlr4 Python package not found: {e}')
except Exception as e:
    print(f'✗ antlr4 Python package error: {e}')
"
echo ""

# Test 3: Check antlr4-python3-runtime package
echo "3. Testing antlr4-python3-runtime package:"
python -c "
try:
    import antlr4_python3_runtime
    print('✓ antlr4-python3-runtime imported successfully')
    print(f'antlr4-python3-runtime location: {antlr4_python3_runtime.__file__}')
except ImportError as e:
    print(f'✗ antlr4-python3-runtime not found: {e}')
except Exception as e:
    print(f'✗ antlr4-python3-runtime error: {e}')
"
echo ""

# Test 4: Check pip list for antlr4 packages
echo "4. Checking pip list for antlr4 packages:"
pip list | grep -i antlr
echo ""

# Test 5: Check which antlr4
echo "5. Testing 'which antlr4':"
which antlr4
echo ""

# Test 6: Check antlr4 version with different methods
echo "6. Testing antlr4 version methods:"
echo "Method 1 - antlr4 --version:"
antlr4 --version 2>/dev/null || echo "Command not found or failed"

echo ""
echo "Method 2 - python -c 'import antlr4; print(antlr4.__version__)':"
python -c "
try:
    import antlr4
    print(antlr4.__version__)
except AttributeError:
    print('No __version__ attribute found')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "Method 3 - pip show antlr4-python3-runtime:"
pip show antlr4-python3-runtime 2>/dev/null || echo "Package not found"

echo ""
echo "=== ANTLR4 TEST COMPLETED ===" 