# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a PDF prepress toolkit called "Paul's Preponderating Prepresser" (PPP), version 1.1.1. It is packaged as an installable Python package (`ppp-prepress`) that can be installed system-wide via `pipx install .` on both macOS and Linux.

**Version 1.1.1: Proper Python packaging**
- Restructured as `src/ppp/` package with `pyproject.toml`
- All CLI tools installed as entry points (no shebangs, no PATH hacking)
- Bash scripts rewritten as Python in `src/ppp/shell.py`
- Padding PDFs bundled as package data via `importlib.resources`
- Old standalone scripts preserved in `old/` for reference

## Key Dependencies

- **PyPDF2**: Core PDF manipulation library used throughout
- **pdftk**: External command-line tool for PDF operations (splitting, merging, compression)
- **poppler-utils**: Provides `pdftops` for PDF to PostScript conversion
- **psutils**: Provides `psbook` and `pstops` for PostScript manipulation (page reordering and imposition)
- **ghostscript**: Provides `ps2pdf` for PostScript to PDF conversion

## Architecture

### Package Structure

```
src/ppp/
  __init__.py          # Version string
  _util.py             # Shared data-file lookup via importlib.resources
  workflow.py          # Main workflow orchestrator (entry point: ppp)
  printydump.py        # Manual signature splitter (entry point: printydump)
  pad.py               # PDF padding utility (entry point: ppp-pad)
  merge.py             # PDF merger (entry point: pdfmerge)
  shell.py             # Python ports of bash scripts (singledingle, flippar, etc.)
  data/                # Bundled padding PDFs (1pp.pdf-7pp.pdf, 1LTRpp.pdf)
```

### Core Workflow: Signature-Based Printing

The toolkit implements a complete prepress workflow for bookbinding:

1. **Signature Division** (`ppp.workflow`, `ppp.printydump`): Split a PDF into signatures
2. **Page Reordering** (psbook): Rearrange pages so they print in correct order when folded
3. **Imposition** (pstops): Arrange multiple pages on single sheets for efficient printing
4. **Format Conversion**: PDF → PS → PDF pipeline for applying PostScript-based transformations

### Signature Tables

`workflow.py` and `printydump.py` define signature lookup tables (sig4 through sig48) mapping page ranges for different signature sizes.

### External Dependencies

- **pdftools** (pip package): Provides `pdf_merge()` and argument parsing, used by `merge.py`
- **PyPDF2** (pip package): Core PDF reading/manipulation

## Common Commands

All commands are installed system-wide via `pipx install .` and can be run from any directory.

### Main Workflow
```bash
ppp [source.pdf]
```
Orchestrates the complete workflow: analyzes PDF, suggests signature configs, pads, splits, imposes, and combines.

### Other Commands
```bash
ppp-pad source.pdf [output.pdf] [multiple]   # Pad to multiple of 4
printydump                                    # Manual signature splitting
pdfmerge -o output.pdf input1.pdf input2.pdf  # Merge PDFs
singledingle file.pdf                         # 2-up imposition
flippar file.pdf                              # Fix flipped back pages
fppp                                          # Batch singledingle (all PDFs in cwd)
pppf                                          # Batch flippar (all PDFs in cwd)
impose-4up file.pdf                           # 4-up imposition
isbnner                                       # Set Calibre ISBN metadata
```

## Development Notes

### File Naming Conventions

- **PPPworking.pdf**: Temporary file created when page count corrections are applied
- **sig##.pdf**: Raw signature files (## = zero-padded number)
- **s##b.ps**: PostScript files after psbook reordering
- **s##i.ps**: PostScript files after imposition
- **s##PPP.pdf**: Final processed signature PDFs
- **PPP[name].pdf**: General prefix for processed output files

### Working with Signatures

When modifying signature handling:
1. Page numbers in signature tables are 1-indexed (PDF standard)
2. Signature sizes must be multiples of 4 (bookbinding requirement)
3. Maximum 30 signatures per document (hardcoded limit)
4. Maximum 960 pages total (30 signatures × 32 pages)

### Data File Resolution

Padding PDFs are bundled in `src/ppp/data/` and resolved via `ppp._util.get_data_path()`. This checks the current working directory first (allowing user overrides), then falls back to the package data directory. Uses `importlib.resources` for reliable cross-platform resolution.

### Installation

```bash
pipx install .           # Install system-wide (recommended)
pip install -e .         # Editable install for development
./install.sh             # Full install including system dependencies
```

## Testing

No automated test suite exists yet. Test manually with the included `lipsum-8.pdf` and `lipsum64.pdf` example files.
