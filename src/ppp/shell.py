"""
Python wrappers for the bash-based PostScript pipeline tools.
These replace the original bash scripts (singledingle, flippar, etc.)
so everything can be installed via a single `pipx install`.
"""

import glob
import os
import subprocess
import shutil
import sys


def _run(cmd, description=None):
    """Run a command, printing errors on failure."""
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        tool = cmd[0]
        print(f'ERROR: {tool} not found.')
        if sys.platform == 'darwin':
            hints = {
                'pdftops': 'brew install poppler',
                'psbook': 'brew install psutils',
                'pstops': 'brew install psutils',
                'ps2pdf': 'brew install ghostscript',
                'calibredb': 'brew install calibre',
            }
        else:
            hints = {
                'pdftops': 'sudo apt install poppler-utils',
                'psbook': 'sudo apt install psutils',
                'pstops': 'sudo apt install psutils',
                'ps2pdf': 'sudo apt install ghostscript',
                'calibredb': 'sudo apt install calibre',
            }
        if tool in hints:
            print(f'Install it with: {hints[tool]}')
        sys.exit(1)
    except subprocess.CalledProcessError:
        if description:
            print(f'ERROR: {description} failed')
        sys.exit(1)


def _cleanup_ps():
    """Remove all .ps files in current directory."""
    for f in glob.glob('*.ps'):
        os.remove(f)


def _cowsay(message):
    """Run cowsay if available, otherwise just print."""
    if shutil.which('cowsay'):
        subprocess.run(['cowsay', message])
    else:
        print(message)


def singledingle(filename):
    """Single-sided 2-up imposition: PDF -> PS -> psbook -> pstops -> PDF."""
    base = filename.removesuffix('.pdf')

    print(f'got file {filename}')
    print('.PSenating ...')
    _run(['pdftops', '-level3', '-origpagesizes', filename, f'{base}.ps'])

    print(' ... rearranging pages ...')
    _run(['psbook', f'{base}.ps', f'b{base}.ps'])

    print(' ... imposing pages 2-up ...')
    _run(['pstops', '2:0L@1.0(1w,0)+1L@1.0(1w,0.5h)', f'b{base}.ps', f'i{base}.ps'])

    print(' ... re.PDFenating ...')
    _run(['ps2pdf', f'i{base}.ps', f'PPP{base}.pdf'])

    _cleanup_ps()
    _cowsay('and boom goes the dynamite.')


def singledingle_main():
    if len(sys.argv) < 2:
        print('Usage: singledingle <file.pdf>')
        sys.exit(1)
    singledingle(sys.argv[1])


def flippar(filename):
    """Page flip fixer: PDF -> PS -> pstops -> PDF."""
    base = filename.removesuffix('.pdf')

    print(f'got file {filename}')
    print('.PSenating ...')
    _run(['pdftops', '-level3', '-origpagesizes', filename, f'{base}.ps'])

    print(' ... reticulating splines ...')
    _run(['pstops', '2:0,1U(1w,1h)', f'{base}.ps', f'i{base}.ps'])

    print(' ... re.PDFenating ...')
    _run(['ps2pdf', f'i{base}.ps', f'{base}-fixed.pdf'])

    _cleanup_ps()
    _cowsay('and boom goes the dynamite.')


def flippar_main():
    if len(sys.argv) < 2:
        print('Usage: flippar <file.pdf>')
        sys.exit(1)
    flippar(sys.argv[1])


def fppp_main():
    """Run singledingle on all PDFs in current directory."""
    pdf_files = sorted(glob.glob('*.pdf'))
    if not pdf_files:
        print('No PDF files found in current directory.')
        sys.exit(1)
    for f in pdf_files:
        singledingle(f)


def pppf_main():
    """Run flippar on all PDFs in current directory."""
    pdf_files = sorted(glob.glob('*.pdf'))
    if not pdf_files:
        print('No PDF files found in current directory.')
        sys.exit(1)
    for f in pdf_files:
        flippar(f)


def impose_4up(filename):
    """4-up imposition: PDF -> PS -> pstops -> PDF."""
    base = filename.removesuffix('.pdf')

    print(f'got file {filename}')
    print('.PSenating ...')
    _run(['pdftops', '-level3', '-origpagesizes', filename, f'{base}.ps'])

    print(' ... imposing pages 4-up ...')
    _run(['pstops',
          '4:0U(0,0)+7U(0.5w,0)+3(0,0.5h)+4(0.5w,0.5h), 4:6U(0,0)+1U(0.5w,0)+5(0,0.5h)+2(0.5w,0.5h)',
          f'{base}.ps', f'i{base}.ps'])

    print(' ... re.PDFenating ...')
    _run(['ps2pdf', f'i{base}.ps', f'PPP{base}.pdf'])

    _cleanup_ps()
    _cowsay('and boom goes the dynamite.')


def impose_4up_main():
    if len(sys.argv) < 2:
        print('Usage: impose-4up <file.pdf>')
        sys.exit(1)
    impose_4up(sys.argv[1])


def isbnner_main():
    """Set ISBN metadata on a Calibre book entry."""
    isbn = input('ISBN to add: ').strip()
    theid = input('ID to add it to: ').strip()

    _run(['calibredb', 'set_metadata', '--field', f'identifiers:isbn:{isbn}', theid])

    go = input('AGAIN???!??!   ').strip()
    if go not in ('Y', 'y'):
        return

    isbn = input('ISBN to add: ').strip()
    theid = input('ID to add it to: ').strip()
    _run(['calibredb', 'set_metadata', '--field', f'identifiers:isbn:{isbn}', theid])
