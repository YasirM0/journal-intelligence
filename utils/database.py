from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "journals.csv"


def load_journals() -> pd.DataFrame:
    """
    Load the journal dataset.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing all journals.
    """
    return pd.read_csv(DATA_FILE)