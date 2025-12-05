# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a PDF prepress toolkit called "Paul's Preponderating Prepresser" (PPP), version 1.0. It contains Python scripts and bash utilities for manipulating PDFs in preparation for printing, particularly focused on signature-based book printing workflows.

**Version 1.0 Updates:**
- Added comprehensive input validation and error checking
- Automated page count padding for signature compatibility
- Created unified workflow orchestrator for streamlined operation
- Improved code quality with better error handling and user feedback

## Key Dependencies

- **PyPDF2**: Core PDF manipulation library used throughout
- **pdftk**: External command-line tool for PDF operations (splitting, merging, compression)
- **poppler-utils**: Provides `pdftops` for PDF to PostScript conversion
- **psutils**: Provides `psbook` and `pstops` for PostScript manipulation (page reordering and imposition)
- **ghostscript**: Provides `ps2pdf` for PostScript to PDF conversion

## Architecture

### Core Workflow: Signature-Based Printing

The toolkit implements a complete prepress workflow for bookbinding:

1. **Signature Division** (PPP.py, printydump.py): Split a PDF into signatures (groups of pages that fold together)
2. **Page Reordering** (psbook): Rearrange pages so they print in correct order when folded
3. **Imposition** (pstops): Arrange multiple pages on single sheets for efficient printing
4. **Format Conversion**: PDF → PS → PDF pipeline for applying PostScript-based transformations

### Signature Tables

Multiple scripts define signature lookup tables (sig4, sig8, sig12, sig16, sig20, sig24, sig28, sig32, sig36, sig40, sig44, sig48) mapping page ranges for different signature sizes. These tables store tuples of (start_page, end_page) pairs for extracting signatures from source documents.

### PDF Manipulation Library (pdftools.py)

Provides reusable functions imported by other scripts:
- `pdf_merge()`: Combine multiple PDFs
- `pdf_split()`: Split PDF by page count or sequence
- `pdf_rotate()`: Rotate pages clockwise/counterclockwise
- `pdf_copy()`: Extract specific pages
- `pdf_zip()`: Interleave pages from two PDFs (useful for even/odd page assembly)
- `pdf_insert()`: Insert pages from one PDF into another
- `pdf_remove()`: Remove specific pages
- `pdf_add()`: Append pages from source to destination

## Common Commands

### Recommended: Automated Workflow (v1.0)
```bash
./ppp-workflow.py [source.pdf]
```
**The recommended way to use PPP v1.0.** This orchestrates the complete workflow:
1. Analyzes source PDF and detects page count
2. Suggests optimal signature configurations
3. Automatically pads with blank pages if needed
4. Splits into signatures (sig01.pdf, sig02.pdf, etc.)
5. Optionally imposes signatures 2-up for printing
6. Outputs PPPsig*.pdf files ready for double-sided printing

Interactive and intelligent - handles edge cases automatically.

### Manual Padding (if needed separately)
```bash
./ppp-pad.py source.pdf [output.pdf] [multiple]
```
Automatically adds blank pages to make page count a multiple of 4 (or specified number).
Looks for 1pp.pdf, 2pp.pdf, 3pp.pdf padding files in current or script directory.

### Validated Signature Splitting (v1.0)
```bash
./printydump.py
```
**Now with validation!** Prompts for:
- Source PDF filename (validates existence and readability)
- Signature bulk (4-48 pages, validated against allowed sizes)
- Automatically calculates number of signatures
- Checks page count divisibility and provides helpful error messages
Outputs numbered signature files (sig01.pdf, sig02.pdf, etc.)

### Legacy: Full Prepress Tool (v0.777)
```bash
./PPP.py inputfile.pdf
```
Original interactive workflow (now superseded by ppp-workflow.py):
1. Validates page count (max 960 pages)
2. Auto-corrects page counts to multiples of 4 (using 1pp.pdf, 2pp.pdf, 3pp.pdf)
3. Prompts for signature size (4, 8, 12, 16, 20, 24, 28, 32 pages)
4. Splits into signatures (sig01.pdf, sig02.pdf, etc.)
5. Converts to PostScript, reorders pages, imposes 2-up
6. Converts back to PDF with "PPP" prefix

### PDF Page Counting
```bash
./pagecounts.py
```
Interactive tool to count pages in multiple PDFs and output to counts.txt

### PDF Merging
```bash
./pdfmerge.py -o output.pdf input1.pdf input2.pdf [...]
./pdfmerge.py -o output.pdf -d input1.pdf input2.pdf  # Delete inputs after merge
```

### 2-Up Imposition (Single/Double Sided)
```bash
./singledingle inputfile.pdf    # Single-sided 2-up imposition
./doublebanger inputfile.pdf    # Double-sided 2-up imposition
./cingledingle inputfile.pdf    # Alternative single-sided variant
```
These scripts:
1. Convert PDF → PS (pdftops)
2. Impose 2-up landscape (pstops)
3. Convert back to PDF (ps2pdf)
Output: PPPinputfile.pdf

### Watermark Removal
```bash
./rmwm.py "watermark text" file1.pdf [file2.pdf ...]
```
Uncompresses PDFs, searches for and removes objects containing specified text, recompresses. Outputs .scrubbed.pdf files.

### Batch Processing Scripts

The bash scripts (bookenate, imposenate, pdfenate, psenate) operate on batches of signature files with numbered naming (sig01, sig02, etc.). They iterate through ranges using shell loops.

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

### subprocess.Popen Usage

Many scripts use `subprocess.Popen()` with `stdout=subprocess.PIPE` for external tool calls. This runs commands asynchronously - consider whether synchronous execution (`subprocess.run()` or `subprocess.call()`) would be more appropriate for sequential operations.

### Interactive Input Patterns

Scripts follow a consistent pattern:
- Accept filename argument or prompt interactively
- Handle both "file.pdf" and "file" (auto-append .pdf) inputs
- Confirm before destructive operations
- Provide [y/n] or [option letters] style prompts

## Version 1.0 Improvements

### Input Validation (printydump.py)
- File existence checking before processing
- PDF readability validation with PyPDF2
- Automatic page count detection from PDF
- Signature size validation against allowed values (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
- Page count divisibility checking with helpful error messages
- Automatic calculation of signature count

### Auto-Padding Utility (ppp-pad.py)
- Standalone utility for adding blank pages
- Automatically detects required padding (to multiple of 4 or custom)
- Searches for padding files (1pp.pdf, 2pp.pdf, 3pp.pdf) in multiple locations
- Overwrite protection with user confirmation
- Output verification

### Workflow Orchestrator (ppp-workflow.py)
- Single-command operation from source to print-ready output
- Intelligent signature size suggestions based on page count
- Top 5 configuration recommendations
- Integrated padding for seamless operation
- Optional automatic imposition
- Clear progress feedback throughout process

### Code Quality Improvements
- Replaced `subprocess.Popen()` with `subprocess.run(check=True)` for better error handling
- Consolidated duplicate if/elif chains into dictionary lookups (SIG_TABLES)
- Added comprehensive error messages and user guidance
- f-string formatting for cleaner code

## Testing

### Manual Testing Checklist
Test the v1.0 workflow with:

1. **Valid even-page-count PDF** (e.g., 32 pages)
   - Should split cleanly without padding
   - Verify signature files have correct page ranges

2. **Odd-page-count PDF requiring padding** (e.g., 30 pages)
   - Should suggest padding options
   - Verify padded output has correct total pages
   - Check that blank pages appear at end

3. **Various signature sizes** (4, 8, 12, 16, 24, 32)
   - Test that all signature sizes work correctly
   - Verify page ordering in signatures

4. **Edge cases:**
   - Very small PDFs (4-8 pages)
   - Invalid signature size input (should reject)
   - Non-existent file (should error gracefully)
   - Corrupted PDF (should error gracefully)

5. **Full workflow:**
   - Run ppp-workflow.py on real document
   - Verify imposed output (PPPsig*.pdf)
   - Test print output on actual printer

No automated test suite exists yet (future enhancement).
