import unittest
import pandas as pd
from src.ab_analyzer import ABAnalyzer
from src.data_loader import DataLoader
import os


class TestABAnalyzer(unittest.TestCase):
    def setUp(self):
        self.project_dir = os.getcwd()
        self.raw_data_dir = os.path.join(self.project_dir, "data", "raw", "1")
        self.output_dir = os.path.join(self.project_dir, "tests", "output")
        self.test_analyzer = ABAnalyzer(self.raw_data_dir, self.output_dir)

    def test_data_loading(self):
        self.test_analyzer.load_and_preprocess_data()
        self.assertIsNotNone(self.test_analyzer.data)
        self.assertIsInstance(self.test_analyzer.data, pd.DataFrame)
        self.assertIn("test group", self.test_analyzer.data.columns)
        self.assertIn("converted", self.test_analyzer.data.columns)
        self.assertEqual(self.test_analyzer.data["converted"].dtype, "bool")

    def test_conversion_rate_calculation(self):
        self.test_analyzer.load_and_preprocess_data()
        conversion_rates = self.test_analyzer.stats.calculate_conversion_rate(
            self.test_analyzer.data, "test group", "converted"
        )
        self.assertIsNotNone(conversion_rates)
        self.assertIsInstance(conversion_rates, pd.DataFrame)
        self.assertIn("conversion_rate", conversion_rates.columns)
        self.assertEqual(len(conversion_rates), 2)

    def test_confidence_interval_calculation(self):
        self.test_analyzer.load_and_preprocess_data()
        confidence_intervals = self.test_analyzer.stats.calculate_confidence_interval(
            self.test_analyzer.data, "test group", "converted"
        )
        self.assertIsNotNone(confidence_intervals)
        self.assertIsInstance(confidence_intervals, pd.DataFrame)
        self.assertIn("lower_bound", confidence_intervals.columns)
        self.assertIn("upper_bound", confidence_intervals.columns)
        self.assertIn("conversion_rate", confidence_intervals.columns)
        self.assertEqual(len(confidence_intervals), 2)

    def test_hypothesis_test(self):
        self.test_analyzer.load_and_preprocess_data()
        (
            t_stat,
            p_value,
            is_significant,
        ) = self.test_analyzer.stats.perform_hypothesis_test(
            self.test_analyzer.data, "test group", "converted"
        )
        self.assertIsNotNone(t_stat)
        self.assertIsNotNone(p_value)
        self.assertIsInstance(is_significant, bool)


if __name__ == "__main__":
    unittest.main()
