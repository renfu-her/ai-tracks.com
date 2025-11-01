# Pillow Installation Troubleshooting for Python 3.13

## Problem
Pillow installation fails on Python 3.13 with `KeyError: '__version__'` error.

## Solutions

### Solution 1: Upgrade pip, setuptools, and wheel first
```bash
python -m pip install --upgrade pip setuptools wheel
pip install Pillow
```

### Solution 2: Install latest Pillow version
```bash
pip install --upgrade Pillow
```

### Solution 3: Use pre-built wheel (if available)
```bash
pip install --only-binary :all: Pillow
```

### Solution 4: Install from source with updated build tools
```bash
# Install build dependencies
pip install --upgrade pip setuptools wheel setuptools-scm

# Then install Pillow
pip install Pillow --no-binary :all:
```

### Solution 5: Use Pillow-SIMD (faster alternative)
```bash
pip install Pillow-SIMD
```

### Solution 6: If all else fails, use Python 3.11 or 3.12
Python 3.13 is very new and some packages may not have full support yet.
Consider using Python 3.11 or 3.12 for better compatibility.

## Quick Fix Command
Try this command sequence:
```bash
python -m pip install --upgrade pip setuptools wheel setuptools-scm
pip install Pillow --no-cache-dir
```

## Alternative: Use Pillow without version pinning
If you continue to have issues, remove the version pinning in requirements.txt:
```
Pillow  # Instead of Pillow==10.1.0
```

Then install:
```bash
pip install -r requirements.txt
```

