# SOSCleaner Modernization Tasks

> Migration from Python 2.7 to Python 3.10+, updating deprecated dependencies, modernizing packaging, and updating CI/CD infrastructure.

**Current Version:** 0.4.4
**Target Version:** 0.5.0

---

## Phase 1: Python 3 Migration ✅ COMPLETED

### 1.1 Update Python Shebangs and Encoding ✅
**Files:** `scripts/soscleaner`, `soscleaner/soscleaner.py`, `test_soscleaner.py`, `setup.py`

- [x] Change `#!/usr/bin/env python2` to `#!/usr/bin/env python3` in `scripts/soscleaner`
- [x] Remove `# -*- coding: iso-8859-15 -*-` from `test_soscleaner.py`
- [x] Update `#!/usr/bin/env python` to `#!/usr/bin/env python3` in remaining files

### 1.2 Remove Python 2 Compatibility Imports ✅
**File:** `soscleaner/soscleaner.py`

- [x] Remove `from builtins import str` (line 22)
- [x] Remove `from builtins import range` (line 23)
- [x] Remove `from builtins import object` (line 24)
- [x] Update `class SOSCleaner(object):` to `class SOSCleaner:`

### 1.3 Migrate ipaddr to ipaddress (stdlib) ✅
**Files:** `soscleaner/soscleaner.py`, `test_soscleaner.py`

- [x] Replace `from ipaddr import IPv4Network, IPv4Address, IPv6Network, IPv6Address` with `from ipaddress import ...`
- [x] Update API calls:
  - [x] `network.network.compressed` → `network.network_address.compressed`
  - [x] `network.broadcast` → `network.broadcast_address`
  - [x] Add `strict=False` to `IPv4Network()` calls where needed
- [x] Test all network-related methods:
  - [x] `_ip4_new_obfuscate_net()`
  - [x] `_ip4_parse_network()`
  - [x] `_ip4_network_in_db()`
  - [x] `_ip4_add_network()`
  - [x] `_ip4_find_network()`
  - [x] `_ip4_in_db()`
  - [x] `_ip4_2_db()`

### 1.4 Update optparse to argparse ✅
**File:** `scripts/soscleaner`

- [x] Replace `from optparse import OptionParser` with `import argparse`
- [x] Convert `OptionParser(usage=..., version=...)` to `ArgumentParser()`
- [x] Convert all `parser.add_option()` to `parser.add_argument()`
- [x] Update option handling from `(options, args) = parser.parse_args()` to argparse namespace
- [x] Add `--version` action separately (argparse style)

### 1.5 Fix Python 3 Syntax/API Changes ✅
**Files:** `soscleaner/soscleaner.py`, `test_soscleaner.py`

- [x] Add explicit encoding to `open()` calls: `open(file, 'r', encoding='utf-8')`
- [x] Replace `os.popen()` with `subprocess.run()`
- [x] Fix regex flag placement (`(?i)` must be at start in Python 3.11+)
- [x] Fix `oct()` file mode check in tests (use `stat.S_IMODE()`)
- [x] Verify no `dict.iteritems()` usage (use `dict.items()`) - confirmed none
- [x] Verify no `dict.iterkeys()` usage (use `dict.keys()`) - confirmed none
- [x] Verify all print statements are function calls - confirmed

---

## Phase 2: Dependency Updates ✅ COMPLETED

### 2.1 Update setup.py Dependencies ✅
**File:** `setup.py`

- [x] Remove `ipaddr` from `install_requires`
- [x] Remove `future` from `install_requires`
- [x] Remove `configparser>=4,<5` from `install_requires`
- [x] Add `python_requires='>=3.8'`

### 2.2 Update requirements.txt ✅
**File:** `requirements.txt`

- [x] Remove `ipaddr`
- [x] Remove `nose`
- [x] Remove `simplejson`
- [x] Remove `bumpversion`
- [x] Add `pytest>=7.0`
- [x] Add `pytest-cov>=4.0`
- [x] Keep `coveralls`

### 2.3 Create requirements-dev.txt ✅
**File:** `requirements-dev.txt` (new)

- [x] Add `bump2version`
- [x] Add `mkdocs` or Sphinx dependencies
- [x] Add `build` for package building

---

## Phase 3: Test Framework Migration (nose → pytest) ✅ COMPLETED

### 3.1 Convert Test Class to pytest ✅
**File:** `tests/test_soscleaner.py`

- [x] Keep `unittest.TestCase` (pytest supports it) - kept existing style, all 75 tests pass
- [N/A] Replace assertions (if converting fully) - not needed, unittest.TestCase works with pytest
- [N/A] Convert `setUp`/`tearDown` to pytest fixtures - not needed, current approach works

### 3.2 Update Test Imports ✅
**File:** `tests/test_soscleaner.py`

- [x] Update `from ipaddr import ...` to `from ipaddress import ...`
- [x] Remove `sys.path.append('soscleaner/')` hack
- [x] Update import to `from soscleaner.soscleaner import SOSCleaner`

### 3.3 Move Test File ✅
- [x] Create `tests/` directory
- [x] Move `test_soscleaner.py` to `tests/test_soscleaner.py`
- [x] Create `tests/__init__.py`
- [x] Create `soscleaner/__init__.py` (needed for proper package imports)

---

## Phase 4: Modern Packaging (pyproject.toml) ✅ COMPLETED

### 4.1 Create pyproject.toml ✅
**File:** `pyproject.toml` (new)

- [x] Define `[build-system]` with setuptools
- [x] Define `[project]` metadata (name, version, description, etc.)
- [x] Set `requires-python = ">=3.8"`
- [x] Define `[project.scripts]` entry point for CLI
- [x] Define `[project.optional-dependencies]` for dev/test
- [x] Configure `[tool.pytest.ini_options]`
- [x] Configure `[tool.coverage.run]` and `[tool.coverage.report]`
- [x] Configure `[tool.bumpversion]` (migrated from setup.cfg)

### 4.2 Update Package Structure ✅
- [x] Ensure `soscleaner/soscleaner.py` exports properly
- [x] Add `soscleaner/__init__.py` with version and imports
- [x] Add `soscleaner/__main__.py` for `python -m soscleaner` support
- [x] Create `soscleaner/cli.py` with CLI logic (moved from scripts/soscleaner)

### 4.3 Clean Up Old Config Files ✅
- [x] Minimize `setup.py` (kept as shim for backward compatibility)
- [x] Migrate `setup.cfg` bumpversion config to pyproject.toml
- [x] Remove `.coveragerc` (migrated to pyproject.toml)

---

## Phase 5: CI/CD Migration (Travis CI → GitHub Actions) ✅ COMPLETED

### 5.1 Create Test Workflow ✅
**File:** `.github/workflows/ci.yml` (new)

- [x] Create `.github/workflows/` directory
- [x] Configure trigger on push/PR to master/main
- [x] Set up Python matrix: 3.8, 3.9, 3.10, 3.11, 3.12
- [x] Install dependencies with `pip install -e .[dev]`
- [x] Run `pytest --cov=soscleaner`
- [x] Upload coverage to Coveralls

### 5.2 Create Release Workflow ✅
**File:** `.github/workflows/release.yml` (new)

- [x] Trigger on tag push (v*)
- [x] Build sdist and wheel with `python -m build`
- [x] Publish to PyPI using trusted publishing (id-token: write)
- [x] Publish to TestPyPI first, then PyPI
- [x] Create GitHub Release with artifacts

### 5.3 Remove Old CI Configuration ✅
- [x] Delete `.travis.yml`
- [x] Delete `.copr.enc`
- [x] Update README badges to GitHub Actions

---

## Phase 6: RPM Spec Update ✅ COMPLETED

### 6.1 Update soscleaner.spec for Python 3 ✅
**File:** `soscleaner.spec`

- [x] Remove `Requires: python-ipaddr`
- [x] Change `%{__python2}` to `%{__python3}`
- [x] Change `%py2_install` to `%py3_install`
- [x] Change `%{python2_sitelib}` to `%{python3_sitelib}`
- [x] Update `BuildRequires` for Python 3 (python3-devel, python3-setuptools, python3-pytest)
- [x] Update version to 0.5.0
- [x] Add changelog entry for Python 3 migration
- [x] Add `Requires: python3 >= 3.8`
- [x] Improved %files section with %license and %doc macros
- [x] Updated %description with more detail

---

## Phase 7: Documentation Updates ✅ COMPLETED

### 7.1 Update README.md ✅
**File:** `README.md`

- [x] Update CI badge from Travis to GitHub Actions (done in Phase 5)
- [x] Update Python version requirements (added Requirements section)
- [x] Add note about Python 2 users staying on 0.4.x

### 7.2 Update Sphinx Documentation ✅
**Files:** `docs/*.rst`, `docs/conf.py`

- [x] Update Python version in installation docs (README covers this)
- [x] Update CI/CD link from Travis to GitHub Actions in intro.rst
- [x] Update `docs/conf.py` version to 0.5.0
- [x] Update `docs/conf.py` ci_cd_url extlink to GitHub Actions

### 7.3 Update Version Strings ✅
- [x] `pyproject.toml` → 0.5.0 (done in Phase 4)
- [x] `soscleaner/__init__.py` → 0.5.0 (done in Phase 4)
- [x] `soscleaner/cli.py` → 0.5.0 (done in Phase 4)
- [x] `soscleaner/soscleaner.py` → 0.5.0
- [x] `soscleaner.spec` → 0.5.0 (done in Phase 6)
- [x] `docs/conf.py` → 0.5.0
- [x] `scripts/soscleaner` → delegates to cli.py (no version needed)

---

## Phase 8: Testing and Verification ✅ COMPLETED

### 8.1 Unit Tests ✅
- [x] Run `pytest -v` - all 75 tests pass
- [x] Run `pytest --cov=soscleaner` - 86% code coverage
- [x] Test on Python 3.12 (current environment)
- [N/A] Test on Python 3.8, 3.10 - GitHub Actions CI will test matrix

### 8.2 Integration Tests ✅
- [x] Test with gzip compressed sosreport (test10_extract_sosreport_gz)
- [x] Test with bzip2 compressed sosreport (test11_extract_sosreport_bz)
- [x] Test with xz compressed sosreport (test12_extract_sosreport_xz)
- [x] Test with uncompressed directory (test9_extract_sosreport_dir)
- [x] Verify IP obfuscation works correctly (test31, test35-38)
- [x] Verify hostname obfuscation works correctly (test1-6, test18-23, test48-55)
- [x] Verify MAC address obfuscation works correctly (test58-59, test63, test74)
- [x] Verify keyword obfuscation works correctly (test28-30, test60-61, test66-67)
- [x] Verify user obfuscation works correctly (test39-46, test57, test62, test75)

### 8.3 Package Verification ✅
- [x] Build with `python -m build` - sdist and wheel created successfully
- [x] Install from wheel and test CLI - `soscleaner --version` works
- [x] Install from sdist and test CLI - `soscleaner --version` works
- [x] `python -m soscleaner` entry point works
- [N/A] Build RPM - requires Fedora/RHEL environment

---

## Implementation Order

Recommended sequence:

1. **Phase 1** - Python 3 core migration
2. **Phase 2** - Dependency cleanup
3. **Phase 3** - Test framework (keep tests passing)
4. **Phase 8.1** - Verify tests pass
5. **Phase 4** - Modern packaging
6. **Phase 5** - CI/CD migration
7. **Phase 6** - RPM spec (if needed)
8. **Phase 7** - Documentation
9. **Phase 8.2-8.3** - Final verification

---

## Notes

### Breaking Changes for Users
- Python 2.7 no longer supported (use v0.4.x)
- No functional changes to obfuscation behavior

### Key Risk Areas
1. **ipaddr → ipaddress**: API differences may cause subtle bugs in network handling
2. **optparse → argparse**: CLI behavior should remain identical
3. **Test migration**: Ensure all 75 tests continue to pass

### Files Summary

**Create:**
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`
- `tests/__init__.py`
- `requirements-dev.txt` (optional)

**Modify:**
- `soscleaner/soscleaner.py`
- `scripts/soscleaner`
- `test_soscleaner.py` → `tests/test_soscleaner.py`
- `setup.py`
- `requirements.txt`
- `soscleaner.spec`
- `README.md`
- `docs/conf.py`

**Delete:**
- `.travis.yml`
- `.copr.enc`
- `.coveragerc`
