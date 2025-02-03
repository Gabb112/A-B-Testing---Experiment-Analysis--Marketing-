import pandas as pd
from data_loader import DataLoader
from stats_utils import StatsUtils
from visualization import Visualization
import os


class ABAnalyzer:
    """
    A class to analyze A/B test data and generate insights.
    """

    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.data = None
        self.stats = StatsUtils()
        self.visual = Visualization(os.path.join(self.output_dir, "plots"))
        self.loader = DataLoader(data_dir)

    def load_and_preprocess_data(self) -> None:
        """Loads data and performs basic preprocessing."""
        self.data = self.loader.load_data()
        # Basic preprocessing steps here (if required)
        self.data["converted"] = self.data["converted"].astype(
            bool
        )  # convert to bool type
        print("Data has been loaded and processed.")

    def analyze_ab_test(self) -> None:
        """Performs the analysis, calculating conversion rates, CIs, and t-tests"""
        if self.data is None:
            raise ValueError("Data has not been loaded. Please load data first.")

        # 1. Analyze Conversion Rates
        print("Calculating conversion rates...")
        conversion_rates = self.stats.calculate_conversion_rate(
            self.data, group_col="test group", outcome_col="converted"
        )
        print(f"Conversion rates: \n{conversion_rates}")
        self.visual.plot_conversion_rates(
            conversion_rates, group_col="test group", rate_col="conversion_rate"
        )

        # 2. Calculate Confidence Intervals
        print("Calculating confidence intervals...")
        confidence_intervals = self.stats.calculate_confidence_interval(
            self.data, group_col="test group", outcome_col="converted"
        )
        print(f"Confidence intervals: \n{confidence_intervals}")
        self.visual.plot_confidence_intervals(
            confidence_intervals, group_col="test group"
        )
        # 3. Hypothesis Testing
        print("Performing hypothesis test...")
        t_statistic, p_value, is_significant = self.stats.perform_hypothesis_test(
            self.data, "test group", "converted"
        )
        print(f"T-statistic: {t_statistic}")
        print(f"P-value: {p_value}")
        print(f"Is significant: {is_significant}")

        # 4. Additional Analysis
        print("Performing additional analysis...")
        self.visual.plot_feature_distributions(self.data, "total ads", "test group")
        print("Analysis completed.")

    def run_analysis(self) -> None:
        """Runs all analysis steps"""
        self.load_and_preprocess_data()
        self.analyze_ab_test()


if __name__ == "__main__":
    # Example usage
    project_dir = os.getcwd()
    raw_data_dir = os.path.join(project_dir, "data", "raw", "1")
    output_dir = os.path.join(project_dir, "reports")

    try:
        ab_analyzer = ABAnalyzer(raw_data_dir, output_dir)
        ab_analyzer.run_analysis()
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
