import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from main import intersect_and_annotate


class TestIntersectAndAnnotate(unittest.TestCase):
    def setUp(self):
        self.common_columns = ['chromosome', 'position', 'ref', 'alt']

        self.data_csv = pd.DataFrame({
            'chromosome': ['chr1', 'chr2', 'chr3'],
            'position': [12345, 67890, 13579],
            'ref': ['A', 'T', 'G'],
            'alt': ['G', 'C', 'A'],
        })

        self.enrichment_csv = pd.DataFrame({
            'chromosome': ['chr1', 'chr3', 'chr4'],
            'position': [12345, 13579, 24680],
            'ref': ['A', 'G', 'T'],
            'alt': ['G', 'A', 'C'],
            'info': ['info_1', 'info_2', 'info_3']
        })

    def test_valid_enrichment(self):
        expected_output = pd.DataFrame({
            'chromosome': ['chr1', 'chr2', 'chr3'],
            'position': [12345, 67890, 13579],
            'ref': ['A', 'T', 'G'],
            'alt': ['G', 'C', 'A'],
            'info': ['info_1', None, 'info_2']
        })

        result = intersect_and_annotate(self.data_csv, self.enrichment_csv)

        assert_frame_equal(result, expected_output)

    def test_missing_columns_data_csv(self):
        data_csv_invalid = pd.DataFrame({
            'chromosome': ['chr1'],
            'position': [12345],
        })

        with self.assertRaises(ValueError) as context:
            intersect_and_annotate(data_csv_invalid, self.enrichment_csv)

        self.assertIn('Data_csv is missing required columns.', str(context.exception))

    def test_missing_columns_enrichment_csv(self):
        enrichment_csv_invalid = pd.DataFrame({
            'chromosome': ['chr1'],
            'position': [12345],
            'info': ['info_1']
        })

        with self.assertRaises(ValueError) as context:
            intersect_and_annotate(self.data_csv, enrichment_csv_invalid)

        self.assertIn('Enrichment_csv is missing required columns.', str(context.exception))


if __name__ == "__main__":
    unittest.main()
