#!/usr/bin/env python3

#		        This program is part of
#          Paul's Preponderating Prepresser v1.0
#            (CC-BY-SA) 2025 era vulgaris, by
#        The Rev. Paul T. Fusco-Gessick, J.D., SDA
#                <<paul@neroots.net>>

#                I.F.E.T.  --  I.V.V.S.

"""
Main workflow orchestrator for PDF signature preparation and imposition.
Automates the complete process from source PDF to print-ready signatures.
"""

import sys
import os
import subprocess
import PyPDF2
import shutil

VALID_SIG_SIZES = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]
SIG_TABLES = {
    4: (1,4,5,8,9,12,13,16,17,20,21,24,25,28,29,32,33,36,37,40,41,44,45,48,49,52,53,56,57,60,61,64,65,68,69,72,73,76,77,80,81,84,85,88,89,92,93,96,97,100,101,104,105,108,109,112,113,116,117,120),
    8: (1,8,9,16,17,24,25,32,33,40,41,48,49,56,57,64,65,72,73,80,81,88,89,96,97,104,105,112,113,120,121,128,129,136,137,144,145,152,153,160,161,168,169,176,177,184,185,192,193,200,201,208,209,216,217,224,225,232,233,240),
    12: (1,12,13,24,25,36,37,48,49,60,61,72,73,84,85,96,97,108,109,120,121,132,133,144,145,156,157,168,169,180,181,192,193,204,205,216,217,228,229,240,241,252,253,264,265,276,277,288,289,300,301,312,313,324,325,336,337,348,349,360),
    16: (1,16,17,32,33,48,49,64,65,80,81,96,97,112,113,128,129,144,145,160,161,176,177,192,193,208,209,224,225,240,241,256,257,272,273,288,289,304,305,320,321,336,337,352,353,368,369,384,385,400,401,416,417,432,433,448,449,465,480),
    20: (1,20,21,40,41,60,61,80,81,100,101,120,121,140,141,160,161,180,181,200,201,220,221,240,241,260,261,280,281,300,301,320,321,340,341,360,361,380,381,400,401,420,421,440,441,460,461,480,481,500,501,520,521,540,541,560,561,580,581,600),
    24: (1,24,25,48,49,72,73,96,97,120,121,144,145,168,169,192,193,216,217,240,241,264,265,288,289,312,313,336,337,360,361,384,385,408,409,432,433,456,457,480,481,504,505,528,529,552,553,576,577,600,601,624,625,648,649,672,673,696,697,720,721,744,745,768,769,792,793,816,817,840,841,864,865,888,889,912,913,936,937,960),
    28: (1,28,29,56,57,84,85,112,113,140,141,168,169,196,197,224,225,252,253,280,281,308,309,336,337,364,365,392,393,420,421,448,449,476,477,504,505,532,533,560,561,588,589,616,617,644,645,672,673,700,701,728,729,756,757,784,785,812,813,840,841,868,869,896,897,924,925,952,953,980,981,1008,1009,1036,1037,1064,1065,1092,1093,1120),
    32: (1,32,33,64,65,96,97,128,129,160,161,192,193,224,225,256,257,288,289,320,321,352,353,384,385,416,417,448,449,480,481,512,513,544,545,576,577,608,609,640,641,672,673,704,705,736,737,768,769,800,801,832,833,864,865,896,897,928,929,960,961,992,993,1024,1025,1056,1057,1088,1089,1120,1121,1152,1153,1184,1185,1216,1217,1248,1249,1280,1281,1312,1313,1344,1345,1376,1377,1408,1409,1440,1441,1472,1473,1504,1505,1536,1537,1568,1569,1600),
    36: (1,36,37,72,73,108,109,144,145,180,181,216,217,252,253,288,289,324,325,360,361,396,397,432,433,468,469,504,505,540,541,576,577,612,613,648,649,684,685,720,721,756,757,792,793,828,829,864,865,900,901,936,937,972,973,1008,1009,1044,1045,1080,1081,1116,1117,1152,1153,1188,1189,1224,1225,1260,1261,1296,1297,1332,1333,1368,1369,1404,1405,1440,1441,1476,1477,1512,1513,1548,1549,1584,1585,1620,1621,1656,1657,1692,1693,1728,1729,1764,1765,1800),
    40: (1,40,41,80,81,120,121,160,161,200,201,240,241,280,281,320,321,360,361,400,401,440,441,480,481,520,521,560,561,600,601,640,641,680,681,720,721,760,761,800,801,840,841,880,881,920,921,960,961,1000,1001,1040,1041,1080,1081,1120,1121,1160,1161,1200,1201,1240,1241,1280,1281,1320,1321,1360,1361,1400,1401,1440,1441,1480,1481,1520,1521,1560,1561,1600),
    44: (1,44,45,88,89,132,133,176,177,220,221,264,265,308,309,352,353,396,397,440,441,484,485,528,529,572,573,616,617,660,661,704,705,748,749,792,793,836,837,880,881,924,925,968,969,1012,1013,1056,1057,1100,1101,1144,1145,1188,1189,1232,1233,1276,1277,1320,1321,1364,1365,1408,1409,1452,1453,1496,1497,1540,1541,1584,1585,1628,1629,1672,1673,1716,1717,1760),
    48: (1,48,49,96,97,144,145,192,193,240,241,288,289,336,337,384,385,432,433,480,481,528,529,576,577,624,625,672,673,720,721,768,769,816,817,864,865,912,913,960,961,1008,1009,1056,1057,1104,1105,1152,1153,1200,1201,1248,1249,1296,1297,1344,1345,1392,1393,1440,1441,1488,1489,1536,1537,1584,1585,1632,1633,1680,1681,1728,1729,1776,1777,1824,1825,1872,1873,1920)
}

def get_page_count(filename):
    """Get page count from a PDF file."""
    try:
        with open(filename, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages)
    except Exception as e:
        print(f'ERROR: Could not read PDF file: {e}')
        return None

def suggest_signature_sizes(page_count):
    """
    Suggest optimal signature sizes for a given page count.
    Prefers 32 and 36 page signatures. Never suggests adding >8 blank pages.
    For large padding needs, suggests mixed signature sizes instead.

    Returns list of tuples: (description, sig_sizes_list, pages_to_add)
    where sig_sizes_list is a list of signature sizes (e.g., [32, 32, 32, 28])
    """
    MAX_PADDING = 8
    PREFERRED_SIZES = [32, 36]  # Preferred for stapling
    MAX_SIGNATURES = 40  # Don't suggest absurd numbers of signatures
    MIN_SIG_SIZE = 16 if page_count > 100 else 8  # Use larger sigs for larger docs

    suggestions = []

    # Try preferred sizes first
    for size in PREFERRED_SIZES:
        full_sigs = page_count // size
        remainder = page_count % size

        if remainder == 0:
            # Perfect fit
            desc = f'{full_sigs} × {size}-page signatures'
            sig_config = [size] * full_sigs
            suggestions.append((desc, sig_config, 0))
        else:
            # Option A: Pad to make all signatures the same size (if padding <= 8)
            pages_to_add = size - remainder
            if pages_to_add <= MAX_PADDING:
                desc = f'{full_sigs + 1} × {size}-page signatures'
                sig_config = [size] * (full_sigs + 1)
                suggestions.append((desc, sig_config, pages_to_add))

            # Option B: Use smaller final signature
            # Find best-fitting smaller size for the remainder
            for final_size in reversed([s for s in VALID_SIG_SIZES if s < size]):
                if remainder <= final_size:
                    final_padding = final_size - remainder
                    if final_padding <= MAX_PADDING:
                        desc = f'{full_sigs} × {size}-page + 1 × {final_size}-page'
                        sig_config = [size] * full_sigs + [final_size]
                        suggestions.append((desc, sig_config, final_padding))
                        break  # Take the first (largest) that fits

    # Also try other sizes (non-preferred) as fallback
    for size in [s for s in VALID_SIG_SIZES if s not in PREFERRED_SIZES and s >= MIN_SIG_SIZE]:
        full_sigs = page_count // size
        remainder = page_count % size

        # Skip if it would result in too many signatures
        if full_sigs > MAX_SIGNATURES:
            continue

        if remainder == 0:
            desc = f'{full_sigs} × {size}-page signatures'
            sig_config = [size] * full_sigs
            suggestions.append((desc, sig_config, 0))
        else:
            pages_to_add = size - remainder
            if pages_to_add <= MAX_PADDING and (full_sigs + 1) <= MAX_SIGNATURES:
                desc = f'{full_sigs + 1} × {size}-page signatures'
                sig_config = [size] * (full_sigs + 1)
                suggestions.append((desc, sig_config, pages_to_add))

    # Sort by: 1) least padding, 2) fewest total signatures
    # Remove duplicates by signature configuration
    seen_configs = set()
    unique_suggestions = []
    for desc, sig_config, padding in suggestions:
        config_key = tuple(sig_config)
        if config_key not in seen_configs:
            seen_configs.add(config_key)
            unique_suggestions.append((desc, sig_config, padding))

    unique_suggestions.sort(key=lambda x: (x[2], len(x[1])))  # Sort by padding, then num signatures

    return unique_suggestions[:5]  # Return top 5

def pad_pdf(source_file, pages_to_add):
    """Pad a PDF with blank pages, combining padding files if needed."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    def find_padding_file(filename):
        """Look for a padding file in current dir and script dir."""
        for path in [filename, os.path.join(script_dir, filename)]:
            if os.path.isfile(path):
                return path
        return None

    # Try to find exact padding file first
    exact_file = f'{pages_to_add}pp.pdf'
    exact_path = find_padding_file(exact_file)

    if exact_path:
        # Exact file exists, use it
        padding_files = [exact_path]
    else:
        # Build padding from available files (1pp.pdf, 2pp.pdf, 3pp.pdf)
        # Greedy algorithm: use largest files first
        available = [(3, '3pp.pdf'), (2, '2pp.pdf'), (1, '1pp.pdf')]
        padding_files = []
        remaining = pages_to_add

        for size, filename in available:
            while remaining >= size:
                path = find_padding_file(filename)
                if not path:
                    print(f'ERROR: Cannot create {pages_to_add} blank pages - missing {filename}')
                    return None
                padding_files.append(path)
                remaining -= size

        if remaining > 0:
            print(f'ERROR: Cannot create {pages_to_add} blank pages with available padding files')
            return None

    # Create padded filename
    base, ext = os.path.splitext(source_file)
    output_file = f'{base}-padded{ext}'

    # Run pdftk with all necessary padding files
    print(f'Adding {pages_to_add} blank page(s)...')
    try:
        # Build pdftk command: A=source, B=pad1, C=pad2, etc.
        cmd = ['pdftk', f'A={source_file}']
        labels = []
        for i, pad_file in enumerate(padding_files):
            label = chr(66 + i)  # B, C, D, E, ...
            cmd.append(f'{label}={pad_file}')
            labels.append(label)

        # Cat: A B C D ... output
        cmd.extend(['cat', 'A'] + labels + ['output', output_file])

        subprocess.run(cmd, check=True, capture_output=True)
        print(f'Created {output_file}')
        return output_file
    except subprocess.CalledProcessError as e:
        print(f'ERROR: pdftk failed')
        return None

def split_into_signatures(source_file, sig_sizes):
    """
    Split PDF into signature files.
    sig_sizes can be either:
    - A single integer (uniform signatures)
    - A list of integers (mixed signature sizes)
    """
    page_count = get_page_count(source_file)
    if page_count is None:
        return False

    # Handle both uniform and mixed signatures
    if isinstance(sig_sizes, int):
        sig_sizes = [sig_sizes] * (page_count // sig_sizes)

    # Verify total pages match
    total_pages = sum(sig_sizes)
    if total_pages != page_count:
        print(f'ERROR: Signature sizes ({total_pages} pages) do not match file ({page_count} pages)')
        return False

    print(f'\nSplitting {source_file} into {len(sig_sizes)} signature(s)...')

    current_page = 1
    for i, sig_size in enumerate(sig_sizes, 1):
        end_page = current_page + sig_size - 1
        pagenums = f'{current_page}-{end_page}'
        outputnum = f'sig{str(i).zfill(2)}.pdf'

        try:
            subprocess.run(['pdftk', source_file, 'cat', pagenums, 'output', outputnum],
                         check=True, capture_output=True)
            print(f'  Created {outputnum} ({sig_size} pages)')
        except subprocess.CalledProcessError:
            print(f'  ERROR: Failed to create {outputnum}')
            return False

        current_page = end_page + 1

    return True

def impose_signatures(output_dir):
    """Run singledingle on all signature files and organize output."""
    sig_files = sorted([f for f in os.listdir('.') if f.startswith('sig') and f.endswith('.pdf')])

    if not sig_files:
        print('No signature files found (sig*.pdf)')
        return False

    # Clean up any old PPPsig files from previous runs
    old_imposed = [f for f in os.listdir('.') if f.startswith('PPPsig') and f.endswith('.pdf')]
    if old_imposed:
        print('\nCleaning up old imposed files from previous run...')
        for old_file in old_imposed:
            os.remove(old_file)
            print(f'  Deleted {old_file}')

    print(f'\nImposing {len(sig_files)} signature(s) for 2-up printing...')

    # Check if singledingle is available
    singledingle_path = shutil.which('singledingle')
    if singledingle_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        singledingle_path = os.path.join(script_dir, 'singledingle')
        if not os.path.isfile(singledingle_path):
            print('ERROR: singledingle script not found in PATH or script directory')
            return False

    for sig_file in sig_files:
        print(f'  Imposing {sig_file}...')
        try:
            subprocess.run([singledingle_path, sig_file], check=True)
        except subprocess.CalledProcessError:
            print(f'  ERROR: Failed to impose {sig_file}')
            return False

    print('\nImposition complete!')

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Get list of imposed files
    imposed_files = sorted([f for f in os.listdir('.') if f.startswith('PPPsig') and f.endswith('.pdf')])

    if not imposed_files:
        print('ERROR: No imposed signature files found (PPPsig*.pdf)')
        return False

    # Move and rename imposed files to output directory
    print(f'\nOrganizing files into {output_dir}/')
    for imposed_file in imposed_files:
        # Extract number: PPPsig01.pdf -> 01.pdf
        number = imposed_file.replace('PPPsig', '').replace('.pdf', '')
        new_name = f'{number}.pdf'
        src = imposed_file
        dst = os.path.join(output_dir, new_name)
        shutil.move(src, dst)
        print(f'  {imposed_file} → {output_dir}/{new_name}')

    # Move original signature files to output directory (keep them!)
    print('\nMoving original signature files...')
    for sig_file in sig_files:
        dst = os.path.join(output_dir, sig_file)
        shutil.move(sig_file, dst)
        print(f'  {sig_file} → {output_dir}/{sig_file}')

    return True

def combine_signatures(output_dir):
    """Combine imposed signatures with spacers, limiting to ~200 pages per combined file."""
    PAGES_PER_COMBINED = 200

    # Find spacer file (1LTRpp.pdf)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    spacer_paths = [
        '1LTRpp.pdf',
        os.path.join(script_dir, '1LTRpp.pdf'),
    ]

    spacer_file = None
    for path in spacer_paths:
        if os.path.isfile(path):
            spacer_file = path
            break

    if spacer_file is None:
        print('WARNING: Spacer file (1LTRpp.pdf) not found. Skipping combination.')
        print(f'Looked in: {", ".join(spacer_paths)}')
        return False

    # Get list of imposed signature files in output directory (##.pdf, not sig##.pdf)
    import re
    sig_files = sorted([f for f in os.listdir(output_dir)
                       if f.endswith('.pdf') and re.match(r'^\d+\.pdf$', f)])

    if not sig_files:
        print('ERROR: No signature files found in output directory')
        return False

    print(f'\nCombining signatures with spacers (max {PAGES_PER_COMBINED} pages per file)...')

    # Calculate page counts for each signature
    sig_page_counts = []
    for sig_file in sig_files:
        full_path = os.path.join(output_dir, sig_file)
        page_count = get_page_count(full_path)
        if page_count is None:
            print(f'WARNING: Could not read {sig_file}, skipping')
            continue
        sig_page_counts.append((sig_file, page_count))

    # Get spacer page count (we'll insert it twice for a full double-sided sheet)
    spacer_pages = get_page_count(spacer_file)
    if spacer_pages is None:
        print('ERROR: Could not read spacer file')
        return False

    spacer_pages_total = spacer_pages * 2  # Insert spacer twice

    # Calculate total pages (including spacers)
    total_sig_pages = sum(pc for _, pc in sig_page_counts)
    total_spacer_pages = (len(sig_page_counts) - 1) * spacer_pages_total  # n-1 spacers
    total_pages = total_sig_pages + total_spacer_pages

    # Determine number of batches needed
    import math
    num_batches = math.ceil(total_pages / PAGES_PER_COMBINED)
    target_per_batch = total_pages / num_batches

    # Group signatures into balanced batches
    batches = []
    current_batch = []
    current_pages = 0

    for sig_file, page_count in sig_page_counts:
        # Each signature adds: its pages + spacer pages (except first in batch)
        pages_to_add = page_count + (spacer_pages_total if current_batch else 0)

        # Check if adding this would:
        # 1. Exceed the hard limit of 200 pages, OR
        # 2. Push us significantly over the target (and we have room for another batch)
        would_exceed_limit = current_pages + pages_to_add > PAGES_PER_COMBINED
        over_target = current_pages + pages_to_add > target_per_batch * 1.1  # 10% tolerance
        have_more_batches = len(batches) < num_batches - 1

        if current_batch and (would_exceed_limit or (over_target and have_more_batches)):
            # Start new batch
            batches.append(current_batch)
            current_batch = [(sig_file, page_count)]
            current_pages = page_count
        else:
            current_batch.append((sig_file, page_count))
            current_pages += pages_to_add

    if current_batch:
        batches.append(current_batch)

    print(f'  Creating {len(batches)} combined file(s)...')

    # Create combined files
    for batch_num, batch in enumerate(batches, 1):
        combined_name = f'job{str(batch_num).zfill(2)}.pdf'
        combined_path = os.path.join(output_dir, combined_name)

        # Build pdftk command with spacers between signatures
        cmd = ['pdftk']

        # Add all files as inputs (A=first sig, B=spacer, C=second sig, etc.)
        file_labels = []
        for i, (sig_file, _) in enumerate(batch):
            label = chr(65 + i * 2)  # A, C, E, G, ...
            cmd.append(f'{label}={os.path.join(output_dir, sig_file)}')
            file_labels.append(label)

        # Add spacer as all the even letters (B, D, F, H, ...)
        for i in range(len(batch) - 1):
            label = chr(66 + i * 2)  # B, D, F, H, ...
            cmd.append(f'{label}={spacer_file}')

        # Build cat sequence: A B B C D D E ... (sig, spacer twice, sig, spacer twice, sig)
        cmd.append('cat')
        for i, label in enumerate(file_labels):
            cmd.append(label)
            if i < len(file_labels) - 1:  # Add spacer twice after all but last
                spacer_label = chr(66 + i * 2)
                cmd.append(spacer_label)
                cmd.append(spacer_label)  # Insert spacer twice for full double-sided sheet

        cmd.extend(['output', combined_path])

        # Execute
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            total_pages = sum(pc for _, pc in batch) + (len(batch) - 1) * spacer_pages_total
            print(f'    Created {combined_name} ({len(batch)} signatures, {total_pages} pages)')
        except subprocess.CalledProcessError as e:
            print(f'    ERROR: Failed to create {combined_name}')
            return False

    print(f'\nCombined files created in {output_dir}/')
    return True

def main():
    """Main workflow orchestrator."""
    print('=' * 60)
    print("PAUL'S PREPONDERATING PREPRESSER v1.0")
    print('Automated Workflow for Signature Preparation')
    print('=' * 60)
    print()

    # Get source file
    if len(sys.argv) > 1:
        original_source = sys.argv[1]
    else:
        original_source = input('Source PDF file: ').strip()

    if not original_source.endswith('.pdf'):
        original_source += '.pdf'

    if not os.path.isfile(original_source):
        print(f'ERROR: File "{original_source}" not found.')
        sys.exit(1)

    # Track temporary files for cleanup
    temp_files = []
    source_file = original_source

    # Get page count
    page_count = get_page_count(source_file)
    if page_count is None:
        sys.exit(1)

    # Detect page size
    try:
        with open(source_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            first_page = reader.pages[0]
            mediabox = first_page.mediabox
            width_pts = float(mediabox.width)
            height_pts = float(mediabox.height)
            width_in = width_pts / 72  # Convert points to inches
            height_in = height_pts / 72
    except Exception as e:
        # If we can't detect size, just continue
        width_in = 0
        height_in = 0

    print(f'Source: {source_file}')
    print(f'Pages: {page_count}')
    if width_in > 0 and height_in > 0:
        print(f'Page size: {width_in:.2f}" × {height_in:.2f}"')
    print()

    # Check if source is close to letter size (8.5 × 11 in)
    is_letter_sized = width_in > 7.2 or height_in > 10.0

    if is_letter_sized:
        print('⚠ Large pages detected (close to letter size)')
        print('This document may not need the signature workflow.')
        print()
        print('Options:')
        print('  1. Print as-is on letter-size paper (1-up, double-sided)')
        print('  2. Continue with signature workflow (resize to half-letter)')
        print()
        print('Your choice [1/2]: ', end='')
        size_choice = input().strip()

        if size_choice == '1':
            print()
            print('Suggested workflow for letter-sized document:')
            print('  1. Open PDF in your PDF viewer')
            print('  2. Print double-sided, flip on long edge')
            print('  3. No signature splitting needed!')
            print()
            print('Exiting workflow.')
            sys.exit(0)
        elif size_choice != '2':
            print('Invalid choice. Exiting.')
            sys.exit(1)
        # If choice is 2, continue below

    # Check if source is already 5.5 × 8.5 inches (allow 0.1 inch tolerance)
    is_half_letter = (abs(width_in - 5.5) < 0.1 and abs(height_in - 8.5) < 0.1)

    if is_half_letter:
        print()
        print('✓ Pages are already half-letter size (5.5" × 8.5"), skipping resize step.')
        print()
    else:
        # Ask about resizing to half-letter
        print('Resize pages to half-letter size (5.5 × 8.5 in) first? [y/n] [DEFAULT: yes]: ', end='')
        resize_response = input().strip().lower()

        if resize_response in ['y', 'yes', '']:
            print('Resizing pages to half-letter...')
            base, ext = os.path.splitext(source_file)
            resized_file = f'{base}-halfletter{ext}'

            try:
                # Use ghostscript to resize/fit pages to 5.5 x 8.5 inches
                # 5.5" = 396 points, 8.5" = 612 points (72 points per inch)
                cmd = [
                    'gs',
                    '-sPAPERSIZE=custom',
                    '-dFIXEDMEDIA',
                    '-dPDFFitPage',
                    '-dDEVICEWIDTHPOINTS=396',   # 5.5 inches
                    '-dDEVICEHEIGHTPOINTS=612',  # 8.5 inches
                    '-dNOPAUSE',
                    '-dBATCH',
                    '-dSAFER',
                    '-sDEVICE=pdfwrite',
                    '-sOutputFile=' + resized_file,
                    source_file
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f'Created {resized_file}')

                # Update source to use resized file and track for cleanup
                source_file = resized_file
                temp_files.append(resized_file)

                # Recalculate page count (shouldn't change, but be thorough)
                page_count = get_page_count(source_file)
                if page_count is None:
                    sys.exit(1)

            except subprocess.CalledProcessError as e:
                print('ERROR: ghostscript (gs) failed to resize PDF')
                print('Make sure ghostscript is installed: sudo apt install ghostscript')
                sys.exit(1)
            except FileNotFoundError:
                print('ERROR: ghostscript (gs) not found')
                print('Install it with: sudo apt install ghostscript')
                sys.exit(1)

        print()

    # Handle very small PDFs automatically (≤16 pages)
    if page_count <= 16:
        print('Small PDF detected - processing automatically...')

        # Calculate padding needed to reach next multiple of 4
        if page_count % 4 == 0:
            pages_to_add = 0
            sig_config = [page_count]
            print(f'Configuration: Single {page_count}-page signature (no padding needed)')
        else:
            pages_to_add = 4 - (page_count % 4)
            padded_count = page_count + pages_to_add
            sig_config = [padded_count]
            print(f'Configuration: Single {padded_count}-page signature (adding {pages_to_add} blank pages)')
    else:
        # Normal workflow for larger PDFs
        # Suggest signature sizes
        print('Suggested signature configurations:')
        suggestions = suggest_signature_sizes(page_count)

        if not suggestions:
            print('ERROR: Could not find suitable signature configuration.')
            sys.exit(1)

        # Show suggestions
        for i, (desc, sig_config, pages_to_add) in enumerate(suggestions, 1):
            if pages_to_add == 0:
                print(f'  {i}. {desc} (no padding needed)')
            else:
                print(f'  {i}. {desc} (add {pages_to_add} blank pages)')

        # Get user choice with validation loop
        while True:
            print()
            print(f'Choose a configuration [1-{len(suggestions)}], or q to quit: ', end='')
            choice = input().strip().lower()

            # Check for quit
            if choice in ['q', 'quit']:
                print('Aborted.')
                sys.exit(0)

            # Parse choice
            try:
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(suggestions):
                    desc, sig_config, pages_to_add = suggestions[choice_idx - 1]
                    break  # Valid choice, exit loop
                else:
                    print(f'ERROR: Please choose a number between 1 and {len(suggestions)}, or q to quit.')
                    continue
            except ValueError:
                print('ERROR: Invalid input. Enter a number or q to quit.')
                continue

        print()
        print(f'Configuration: {desc}')
        if pages_to_add > 0:
            print(f'Padding: {pages_to_add} blank page(s) will be added')

    # Pad if needed
    working_file = source_file
    if pages_to_add > 0:
        print()
        working_file = pad_pdf(source_file, pages_to_add)
        if working_file is None:
            sys.exit(1)
        temp_files.append(working_file)

    # Split into signatures
    print()
    if not split_into_signatures(working_file, sig_config):
        sys.exit(1)

    # Create output directory name from source filename
    base_name = os.path.splitext(os.path.basename(source_file))[0]
    output_dir = f'{base_name}-output'

    # Ask about imposition
    print()
    print('Split complete! Would you like to impose the signatures now? [y/n] [DEFAULT: yes]: ', end='')
    response = input().strip().lower()

    if response in ['y', 'yes', '']:
        if not impose_signatures(output_dir):
            sys.exit(1)

        # Clean up temporary files
        for temp_file in temp_files:
            if os.path.isfile(temp_file):
                os.remove(temp_file)

        # Only ask about combining if there are multiple signatures
        if len(sig_config) > 1:
            # Ask about combining
            print()
            print('Would you like to combine signatures with spacers for easier printing? [y/n] [DEFAULT: yes]: ', end='')
            combine_response = input().strip().lower()

            if combine_response in ['y', 'yes', '']:
                if combine_signatures(output_dir):
                    print(f'\n✓ All files ready in {output_dir}/')
                    print('  - Individual signatures: 01.pdf, 02.pdf, ...')
                    print('  - Print jobs: job01.pdf, job02.pdf, ...')
                else:
                    print(f'\n✓ Individual signatures ready in {output_dir}/')
            else:
                print(f'\n✓ Individual signatures ready in {output_dir}/')
        else:
            # Single signature - no need to combine
            print(f'\n✓ Single signature ready in {output_dir}/')
    else:
        # User declined imposition - move sig files to output dir anyway
        print()
        print('Organizing signature files...')
        os.makedirs(output_dir, exist_ok=True)

        sig_files = sorted([f for f in os.listdir('.') if f.startswith('sig') and f.endswith('.pdf')])
        for sig_file in sig_files:
            dst = os.path.join(output_dir, sig_file)
            shutil.move(sig_file, dst)
            print(f'  {sig_file} → {output_dir}/{sig_file}')

        # Clean up temporary files
        for temp_file in temp_files:
            if os.path.isfile(temp_file):
                os.remove(temp_file)

        print(f'\n✓ Signature files ready in {output_dir}/')
        print('  To impose later:')
        print(f'    cd {output_dir}')
        print(f'    fppp')

    print()
    print('Workflow complete!')

if __name__ == '__main__':
    main()
