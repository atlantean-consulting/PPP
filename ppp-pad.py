#!/usr/bin/env python3

#		        This program is part of
#          Paul's Preponderating Prepresser v1.0
#            (CC-BY-SA) 2025 era vulgaris, by
#        The Rev. Paul T. Fusco-Gessick, J.D., SDA
#                <<paul@neroots.net>>

#                I.F.E.T.  --  I.V.V.S.

"""
Auto-padding utility for PDF signature preparation.
Adds blank pages to make page count a multiple of 4.
"""

import sys
import os
import subprocess
import PyPDF2

def get_page_count(filename):
    """Get page count from a PDF file."""
    try:
        with open(filename, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages)
    except Exception as e:
        print(f'ERROR: Could not read PDF file: {e}')
        return None

def pad_pdf(source_file, output_file=None, target_multiple=4):
    """
    Pad a PDF to make its page count a multiple of target_multiple.

    Args:
        source_file: Input PDF filename
        output_file: Output PDF filename (default: padded-{source_file})
        target_multiple: Target multiple for page count (default: 4)

    Returns:
        True if padding was successful or unnecessary, False otherwise
    """
    # Check if source file exists
    if not os.path.isfile(source_file):
        print(f'ERROR: Source file "{source_file}" not found.')
        return False

    # Get page count
    page_count = get_page_count(source_file)
    if page_count is None:
        return False

    print(f'Source file: {source_file}')
    print(f'Current page count: {page_count}')

    # Check if padding is needed
    remainder = page_count % target_multiple
    if remainder == 0:
        print(f'Page count is already a multiple of {target_multiple}. No padding needed.')
        return True

    # Calculate pages to add
    pages_to_add = target_multiple - remainder
    padding_file = f'{pages_to_add}pp.pdf'

    # Check if padding file exists
    # Look in current directory and in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    padding_paths = [
        padding_file,  # Current directory
        os.path.join(script_dir, padding_file),  # Script directory
    ]

    padding_path = None
    for path in padding_paths:
        if os.path.isfile(path):
            padding_path = path
            break

    if padding_path is None:
        print(f'ERROR: Padding file "{padding_file}" not found.')
        print(f'Looked in: {", ".join(padding_paths)}')
        return False

    # Set output filename
    if output_file is None:
        base, ext = os.path.splitext(source_file)
        output_file = f'padded-{base}{ext}'

    # Check if output file already exists
    if os.path.isfile(output_file):
        response = input(f'Output file "{output_file}" already exists. Overwrite? [y/n]: ').strip().lower()
        if response not in ['y', 'yes']:
            print('Aborted.')
            return False

    # Run pdftk to concatenate
    print(f'Adding {pages_to_add} blank page(s) from {padding_file}...')
    try:
        cmd = ['pdftk', f'A={source_file}', f'B={padding_path}', 'cat', 'A', 'B', 'output', output_file]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Verify the output
        new_page_count = get_page_count(output_file)
        if new_page_count == page_count + pages_to_add:
            print(f'Success! Created {output_file} with {new_page_count} pages.')
            return True
        else:
            print(f'WARNING: Expected {page_count + pages_to_add} pages but got {new_page_count}.')
            return False

    except subprocess.CalledProcessError as e:
        print(f'ERROR: pdftk failed: {e.stderr}')
        return False
    except Exception as e:
        print(f'ERROR: {e}')
        return False

def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print('Usage: ppp-pad.py <input.pdf> [output.pdf] [target_multiple]')
        print('')
        print('Automatically pads a PDF with blank pages to make page count')
        print('a multiple of target_multiple (default: 4)')
        print('')
        print('Examples:')
        print('  ppp-pad.py book.pdf                 # Creates padded-book.pdf')
        print('  ppp-pad.py book.pdf ready.pdf       # Creates ready.pdf')
        print('  ppp-pad.py book.pdf ready.pdf 32    # Pad to multiple of 32')
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    target_multiple = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    success = pad_pdf(source_file, output_file, target_multiple)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
