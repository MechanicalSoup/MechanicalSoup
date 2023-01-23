"""Add the main directory of the project to sys.path, so that
uninstalled version is tested.
"""

import os
import sys

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJ_DIR = os.path.dirname(TEST_DIR)

sys.path.insert(0, os.path.join(PROJ_DIR))
