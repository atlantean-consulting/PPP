# Release Notes
... for version 1.1.1

* **Repackaged as a proper Python package** (`ppp-prepress`). Install system-wide with `pipx install .` — no more hardcoded shebangs, no more PATH hacks, no more venv activation. Works identically on macOS and Linux.
* All bash scripts (singledingle, flippar, fppp, pppf, impose-4up, isbnner) rewritten as Python entry points. One `pipx install` gives you everything.
* Padding PDFs (1pp.pdf through 7pp.pdf, 1LTRpp.pdf) bundled as package data via `importlib.resources`. They resolve automatically no matter where you run the commands from.
* `install.sh` updated to use `pipx` instead of manually creating venvs and rewriting shebangs.
* Old standalone scripts moved to `old/` for reference.

---

# Release Notes
... for version 1.1

* Added macOS support. PPP now runs on Linux *and* macOS out of the box.
* Added `install.sh` -- a one-shot installer that detects your OS and installs all system dependencies (via Homebrew on macOS, apt on Linux) plus Python packages.
* Added `requirements.txt` for Python dependencies (`PyPDF2`, `pdftools`).
* Fixed platform-specific error messages: ghostscript install instructions now show the correct command for your OS.
* Bumped version numbers across all scripts.

---

# Release Notes
... for version 1.0

PPP was my *very first* Python project, all the way back in 2015 ... before the dark times ... before the Empire. Now it's all grown up, and so am I. Witness the changes that hath been wrought in order to bring it to this here debut release:

* Automated the whole-ass workflow, including:
* Input validation and error handling.
* A utility that automatically pads yer files to make them multiples of 4.
* A smarty-pants signature size suggestor.
* A convenient output directory for your pleasure.
* A handy batch combiner so you don't have to submit a billion discrete print jobs, thus making your printing efforts more ... discrete

I hope you enjoy :)

-- Paul
