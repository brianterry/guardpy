# guardpy (scaffold)

Python bindings for AWS CloudFormation Guard powered by Rust + pyo3.

## Build (local)

```bash
# Requires Rust toolchain and maturin
pip install maturin
cd guardpy
maturin develop  # builds and installs into current Python env

# Notes:
# - Uses PyO3 0.22 with abi3 (py>=3.9) so Python 3.13 is supported
# - If building against a specific interpreter, use: maturin develop --python $(which python)
```

## Usage

```python
import guardpycfn
res = guardpy.validate_with_guard("AWSTemplateFormatVersion: '2010-09-09'\nResources: {}\n", None)
print(res)
```

## Next steps
- Link to Guard engine (guard-ffi or internal crates)
- Map Guard results to structured matches
- Package wheels for macOS/Linux via maturin

## Test the release wheel locally

Use Python 3.13 to build and audit the wheel.

```bash
python -m pip install maturin==1.16.0 abi3audit==0.0.26
maturin build --release --out wheelhouse
abi3audit --strict wheelhouse/*.whl
python -m pip install --no-index --no-deps wheelhouse/*.whl
python -X faulthandler -m unittest discover -s tests -p 'test_wheel.py' -v
```

The tests import `guardpy`, as built by the current source. Set
`GUARDPY_MODULE=guardpycfn` to run the same tests against the published
`guardpycfn` package.

The release workflow builds each wheel once, audits its stable ABI, and tests
the installed wheel on Python 3.13, 3.14, and 3.15. Linux also tests the Python
3.9 ABI baseline. Publishing uploads these verified files without rebuilding
them. A corrected release must use a new package version: existing PyPI files
cannot be replaced.
