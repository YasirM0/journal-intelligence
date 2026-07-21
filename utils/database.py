"""
Database utilities.

Responsible for loading the journal dataset used by Journal Intelligence.
"""

from pathlib import Path

import pandas as pd


# ==========================================================
# Dataset Location
# ==========================================================

DATA_FILE = Path(__file__).parent.parent / "data" / "journals.csv"


# ==========================================================
# Load Journal Dataset
# ==========================================================

def load_journals() -> pd.DataFrame:
    """
    Load the journal dataset.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing all journals.
    """
    return pd.read_csv(DATA_FILE)