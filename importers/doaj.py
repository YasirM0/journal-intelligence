"""
DOAJ importer.
"""
import pandas as pd

from importers.csv_importer import CSVImporter
from importers.mappings.doaj import DOAJ_COLUMNS
from models.journal import Journal
from services.repository import insert_journals


class DOAJImporter(CSVImporter):
    """
    Import journal metadata from the official DOAJ CSV dataset.
    """

    def __init__(self, csv_path):
        super().__init__(
            source="DOAJ",
            csv_path=csv_path,
        )

    def transform(self, dataframe):
        """
        Convert a DOAJ DataFrame into Journal objects.
        """

        journals = []

        for _, row in dataframe.iterrows():

            mapped = {}

            for internal_name, doaj_column in DOAJ_COLUMNS.items():
                value = row[doaj_column]

                if pd.isna(value):
                    value = None

                mapped[internal_name] = value

            mapped["source"] = self.source

            journal = Journal(**mapped)

            journals.append(journal)

        return journals

    def save(self, journals):
        insert_journals(journals)