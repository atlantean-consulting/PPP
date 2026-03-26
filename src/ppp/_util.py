"""Shared utilities for locating bundled data files."""

import os
from importlib.resources import files


def get_data_path(filename):
    """Resolve a bundled data file, checking cwd first for user overrides."""
    # Check current working directory first (user can override with local files)
    if os.path.isfile(filename):
        return filename
    # Then check package data
    resource_path = str(files('ppp.data').joinpath(filename))
    if os.path.isfile(resource_path):
        return resource_path
    return None
