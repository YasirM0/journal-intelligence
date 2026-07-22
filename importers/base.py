"""
Base classes for journal importers.
"""


class BaseImporter:
    """
    Parent class for all journal importers.

    Every importer follows the same workflow:
    fetch -> transform -> validate -> save
    """

    def __init__(self, source):
        self.source = source
        self.journals = []

    def fetch(self):
        """
        Retrieve raw journal data from the source.
        """
        raise NotImplementedError

    def transform(self, raw_data):
        """
        Convert raw data into the Journal Intelligence schema.
        """
        return raw_data

    def validate(self, journals):
        """
        Validate imported journal data.
        """
        return journals

    def save(self, journals):
        """
        Save validated journals.
        """
        raise NotImplementedError

    def run(self):
        """
        Execute the complete import workflow.
        """

        raw_data = self.fetch()

        journals = self.transform(raw_data)

        journals = self.validate(journals)

        self.save(journals)