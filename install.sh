#!/bin/bash

# ================================================ #
#   This program is part of
#   Paul's Preponderating Prepresser v1.1
#   (CC-BY-SA 4.0) 2025 e.v. by
#   The Rev. Paul T. Fusco-Gessick, J.D., SDA
#   <<paul@neroots.net>>

#   I.F.E.T.  --  I.V.V.S.
# ================================================ #

set -e

OS="$(uname -s)"

echo "======================================================"
echo "  Paul's Preponderating Prepresser v1.1 -- Installer"
echo "======================================================"
echo ""

install_macos() {
    echo "Detected: macOS"
    echo ""

    # Check for Homebrew
    if ! command -v brew &>/dev/null; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew: OK"
    fi

    echo ""
    echo "Installing system dependencies via Homebrew..."
    brew install pdftk-java   # pdftk
    brew install poppler       # pdftops
    brew install psutils       # psbook, pstops
    brew install ghostscript   # gs, ps2pdf
    brew install cowsay
}

install_linux() {
    echo "Detected: Linux"
    echo ""
    echo "Installing system dependencies via apt..."
    sudo apt-get update
    sudo apt-get install -y \
        pdftk \
        poppler-utils \
        psutils \
        ghostscript \
        cowsay \
        python3-venv
}

case "$OS" in
    Darwin)
        install_macos
        ;;
    Linux)
        install_linux
        ;;
    *)
        echo "ERROR: Unsupported operating system: $OS"
        echo "Please install the following tools manually:"
        echo "  pdftk, pdftops (poppler), psbook/pstops (psutils), ghostscript, cowsay"
        exit 1
        ;;
esac

echo ""
echo "Setting up Python virtual environment..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -m venv "$SCRIPT_DIR/.venv"
"$SCRIPT_DIR/.venv/bin/pip" install --quiet -r "$SCRIPT_DIR/requirements.txt"
echo "Python dependencies installed."

echo ""
echo "Updating script interpreters to use virtual environment..."
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python3"
for script in ppp.py ppp-pad.py printydump.py pdfmerge.py; do
    f="$SCRIPT_DIR/$script"
    [ -f "$f" ] && perl -pi -e "s|^#!.*python.*|#!$VENV_PYTHON|" "$f" && echo "  Updated $script"
done

echo ""
echo "======================================================"
echo "  Installation complete!"
echo ""
echo "  Run ./ppp.py to start the workflow."
echo "======================================================"
