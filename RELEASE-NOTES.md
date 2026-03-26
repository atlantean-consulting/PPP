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
