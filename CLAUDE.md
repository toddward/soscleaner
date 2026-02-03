# CLAUDE.md - SOSCleaner Project Guide

This file provides context for Claude (or other AI assistants) working on the SOSCleaner codebase.

## Project Overview

**SOSCleaner** is a Python CLI tool and library that obfuscates sensitive information in datasets, particularly Red Hat sosreports. It consistently replaces sensitive data (IPs, hostnames, MACs, usernames, keywords) with obfuscated values while maintaining data relationships for debugging purposes.

- **License:** GPLv2+
- **Author:** Jamie Duncan (jduncan@redhat.com)
- **Repository:** https://github.com/jduncan-rva/soscleaner
- **Documentation:** https://soscleaner.readthedocs.io

## Architecture

### Single-Class Design

The entire application is contained in one class: `SOSCleaner` in `soscleaner/soscleaner.py` (~1,660 lines). This is intentional for simplicity but could be modularized in the future.

### Key Data Structures

The class maintains several "databases" (dictionaries/lists) that map original values to obfuscated values:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `net_db` | list | Network objects for IP obfuscation |
| `ip_db` | list | Individual IP address mappings |
| `hn_db` | dict | Hostname → obfuscated hostname |
| `dn_db` | dict | Domain name → obfuscated domain |
| `mac_db` | dict | MAC address → obfuscated MAC |
| `kw_db` | dict | Keyword → obfuscated keyword |
| `user_db` | dict | Username → obfuscated username |

### Processing Pipeline

1. **Initialization** (`__init__`) - Set up defaults and databases
2. **Config Loading** (`_read_early_config_options`, `_read_later_config_options`) - Load `/etc/soscleaner.conf`
3. **Environment Prep** (`_prep_environment`) - Create working directories
4. **Extraction** (`_extract_sosreport`) - Decompress tarball (gzip/bzip2/xz)
5. **Data Collection** - Parse routes, hostnames, users from sosreport
6. **File Walking** (`_walk_report`) - Iterate through all files
7. **Line Cleaning** (`_clean_line`) - Apply all obfuscation patterns
8. **Report Generation** (`_create_reports`) - Write mapping CSVs
9. **Archive Creation** (`_create_archive`) - Repack as tarball

### Obfuscation Methods

Each data type has its own subsystem:

- **Networks/IPs** (`_ip4_*`, `_sub_ip`): Network-aware obfuscation preserving subnet structure
- **Hostnames** (`_hn2db`, `_sub_hostname`): FQDN parsing, consistent mapping
- **Domains** (`_dn2db`, `_domains2db`): Multi-level domain handling
- **MACs** (`_mac2db`, `_sub_mac`): Randomized but consistent
- **Keywords** (`_keywords2db`, `_sub_keywords`): User-specified sensitive terms
- **Users** (`_user2db`, `_sub_username`): Username obfuscation from lastlog

## Directory Structure

```
soscleaner/
├── soscleaner/
│   └── soscleaner.py      # Main module (SOSCleaner class)
├── scripts/
│   └── soscleaner         # CLI entry point (argparse-based)
├── test_soscleaner.py     # Unit tests (pytest with unittest.TestCase)
├── docs/                  # Sphinx documentation
├── testdata/              # Test fixtures and sample data
├── setup.py               # Package configuration (legacy, to be replaced)
├── soscleaner.conf        # Example config file
└── soscleaner.spec        # RPM spec file
```

## Development Commands

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=soscleaner --cov-report=term-missing

# Build package
python -m build

# Run the CLI
soscleaner --help
soscleaner -l DEBUG /path/to/sosreport.tar.gz
```

## Testing

Tests are in `test_soscleaner.py` (root directory) using pytest (compatible with unittest.TestCase). 75 tests cover all major functionality.

**Test categories:**
- Environment/setup tests
- Hostname detection (FQDN and non-FQDN)
- File extraction (multiple compression formats)
- Network obfuscation
- Keyword/user/MAC obfuscation
- Report generation

**Test data** is in `testdata/` directory with sample sosreport structures.

## Key Files to Understand

| File | Purpose |
|------|---------|
| `soscleaner/soscleaner.py` | All core logic - start here |
| `scripts/soscleaner` | CLI argument parsing (argparse) |
| `soscleaner.conf` | Config file format example |
| `test_soscleaner.py` | Test coverage shows usage patterns |

## Configuration

SOSCleaner reads `/etc/soscleaner.conf` if present:

```ini
[Default]
loglevel = INFO
root_domain = obfuscateddomain.com
quiet = False

[DomainConfig]
domains = domain1.com,domain2.com

[KeywordConfig]
keywords = secret,password
keyword_files = /path/to/keywords.txt

[NetworkConfig]
networks = 192.168.0.0/16,10.0.0.0/8

[MacConfig]
obfuscate_macs = True
```

## Common Tasks

### Adding a New Obfuscation Type

1. Add database attribute in `__init__` (e.g., `self.new_db = dict()`)
2. Create `_new2db()` method to add entries to database
3. Create `_sub_new()` method to perform regex substitution
4. Add call to `_sub_new()` in `_clean_line()`
5. Create `_create_new_report()` for mapping CSV
6. Add call in `_create_reports()`
7. Add tests in `test_soscleaner.py`

### Modifying Network Obfuscation

Network handling is complex due to subnet awareness. Key methods:
- `_ip4_new_obfuscate_net()` - Creates new obfuscated network
- `_ip4_parse_network()` - Parses CIDR notation
- `_ip4_add_network()` - Adds network to database
- `_ip4_find_network()` - Finds which network an IP belongs to
- `_ip4_2_db()` - Maps original IP to obfuscated IP

### Adding CLI Options

1. Add `parser.add_argument()` in `scripts/soscleaner`
2. Pass option to `cleaner.clean_report(options, sosreport)`
3. Handle in `clean_report()` method or relevant processing method

## Dependencies

**Runtime:**
- Python 3.8+ (uses stdlib `ipaddress`, `configparser`)
- `file` command (for MIME type detection)
- `tar` command (for extraction)
- Root privileges (sosreports are typically root-owned)

**Development:**
- pytest, pytest-cov
- build (for packaging)

## Known Quirks

1. **Root requirement**: Sosreports contain root-owned files; soscleaner warns if not root
2. **False positives list**: Some files (RPM lists, etc.) are skipped to avoid false matches
3. **Binary file detection**: Uses `file` command to skip non-text files
4. **Logging**: Custom `con_out` method for console output during processing

## Modernization Status

See `TASKS.md` for the current modernization roadmap. Key completed/pending items:
- [x] Python 3 migration (from Python 2.7) - **COMPLETED**
- [x] ipaddr → ipaddress stdlib migration - **COMPLETED**
- [x] optparse → argparse migration - **COMPLETED**
- [x] Remove legacy dependencies (ipaddr, future, configparser) - **COMPLETED**
- [ ] nose → pytest migration (tests already work with pytest)
- [ ] Travis CI → GitHub Actions migration
- [ ] setup.py → pyproject.toml migration

## Links

- **Source:** https://github.com/jduncan-rva/soscleaner
- **Issues:** https://github.com/jduncan-rva/soscleaner/issues
- **PyPI:** https://pypi.org/project/soscleaner/
- **Docs:** https://soscleaner.readthedocs.io
- **RPMs:** https://copr.fedorainfracloud.org/coprs/jduncan/soscleaner/
