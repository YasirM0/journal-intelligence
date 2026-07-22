"""
Base importer for CSV-based journal datasets.
"""

from pathlib import Path

import pandas as pd

from importers.base import BaseImporter


class CSVImporter(BaseImporter):
    """
    Base class for journal datasets distributed as CSV files.
    """

    def __init__(self, source, csv_path):
        super().__init__(source)
        self.csv_path = Path(csv_path)

    def fetch(self):
        """
        Load the CSV dataset into a pandas DataFrame.
        """

        return pd.read_csv(self.csv_path)