"""
Database utilities.

Responsible for loading the journal dataset used by Journal Intelligence.
"""

import pandas as pd

from services.repository import get_all_journals


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
    return get_all_journals()