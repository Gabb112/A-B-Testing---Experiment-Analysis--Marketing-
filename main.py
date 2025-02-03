import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
from datetime import datetime


class ABTestAnalyzer:
    """
    A class to perform A/B testing analysis on marketing campaign data.
    """

    def __init__(self, data_dir: str):
        """
        Initializes the ABTestAnalyzer with the directory path containing the data.

        Args:
            data_dir: The directory path where the CSV files are located.
        """
        self.data_dir = data_dir
        self.df = self._load_and_preprocess_data()
        self.alpha = 0.05

    def _load_and_preprocess_data(self) -> pd.DataFrame:
        """
        Loads and preprocesses the A/B testing data, returns a DataFrame.

        Returns:
            DataFrame: A combined and preprocessed DataFrame.
        """
        control_path = os.path.join(self.data_dir, "control_group.csv")
        test_path = os.path.join(self.data_dir, "test_group.csv")

        if not os.path.exists(control_path) or not os.path.exists(test_path):
            raise FileNotFoundError("One or more required data files not found.")

        control_df = pd.read_csv(control_path, sep=';')
        test_df = pd.read_csv(test_path, sep=';')

        # Rename columns for better handling
        control_df.columns = [
            "campaign_name",
            "date",
            "spend",
            "impressions",
            "reach",
            "website_clicks",
            "searches",
            "view_content",
            "add_to_cart",
            "purchase",
        ]
        test_df.columns = [
            "campaign_name",
            "date",
            "spend",
            "impressions",
            "reach",
            "website_clicks",
            "searches",
            "view_content",
            "add_to_cart",
            "purchase",
        ]

        control_df["group"] = "control"
        test_df["group"] = "test"

        combined_df = pd.concat([control_df, test_df], ignore_index=True)
        combined_df["date"] = pd.to_datetime(combined_df["date"], format="%d.%m.%Y")

        if combined_df.isnull().any().any():
            print("Warning: Missing values found. You may wish to handle them using imputing or dropping")

        combined_df.dropna(inplace=True) #drop null values
        combined_df.drop_duplicates(inplace=True)
        return combined_df

    def _calculate_metrics(self) -> pd.DataFrame:
        """
        Calculates key metrics for both groups, and outputs a dataframe with the metrics.

        Returns:
            DataFrame: A DataFrame with calculated metrics.
        """
        metrics = {
            "conversion_rate": "purchase",
            "click_through_rate": "website_clicks",
            "reach": "reach",
            "impressions": "impressions",
            "spend": "spend",
        }

        df_grouped = self.df.groupby("group")
        calculated_metrics = pd.DataFrame()

        for metric, column in metrics.items():
            metric_series = df_grouped.apply(
                lambda x: np.sum(x[column])
                / len(x)
                if metric != "spend"
                else np.mean(x[column])
            )
            calculated_metrics[metric] = metric_series

        return calculated_metrics.reset_index()

    def perform_statistical_analysis(
        self, metric: str, calculated_metrics:pd.DataFrame
    ) -> Tuple[float, float, bool]:
        """
        Performs statistical analysis using a t-test on the input metric.

        Args:
            metric: The metric to analyze between control and test group.
            calculated_metrics: DataFrame with the calculated metrics

        Returns:
            tuple(float, float, bool): the t-statistic, p-value and whether the result is significant
        """

        if metric not in calculated_metrics.columns:
             raise ValueError(f"metric {metric} is not in the list of available metrics")

        control_values = calculated_metrics.loc[calculated_metrics["group"] == "control", metric]
        test_values = calculated_metrics.loc[calculated_metrics["group"] == "test", metric]
        
        t_statistic, p_value = stats.ttest_ind(
            control_values, test_values, equal_var=False
        )

        is_significant = p_value < self.alpha
        return t_statistic, p_value, is_significant

    def visualize_data(self, metrics: List[str]):
        """
        Visualizes the key metrics by plotting them into barplots.

        Args:
            metrics: A list of string of the metrics to visualize.
        """
        calculated_metrics = self._calculate_metrics()
        num_metrics = len(metrics)

        fig, axs = plt.subplots(
            1, num_metrics, figsize=(5 * num_metrics, 5), squeeze=False
        )
        axs = axs.flatten()

        for i, metric in enumerate(metrics):
            if metric not in calculated_metrics.columns:
               print(f"Metric: {metric} is not in the list of calculated metrics, please review the metric name!")
               continue
            sns.barplot(
                x="group",
                y=metric,
                data=calculated_metrics,
                ax=axs[i],
                palette="viridis",
                hue="group",
                legend = False,
            )
            axs[i].set_title(f"Mean {metric} by Group")
            axs[i].set_xlabel("Campaign Group")
            axs[i].set_ylabel(f"Mean {metric}")
        plt.tight_layout()
        plt.show()

    def report_results(self, metrics:List[str]):
        """
        Prints a report of the analysis

        Args:
            metrics: A list of string of the metrics to analyze.
        """
        print("\n--------A/B Testing Results--------\n")

        calculated_metrics = self._calculate_metrics()
        print("Calculated Metrics:")
        print(calculated_metrics.to_string(index=False))

        print("\nStatistical Analysis Results:")
        for metric in metrics:
            t_stat, p_val, is_sig = self.perform_statistical_analysis(metric, calculated_metrics)
            print(
                f"Metric: {metric}, T-Statistic: {t_stat:.2f}, P-Value: {p_val:.3f}, "
                f"Significant: {'Yes' if is_sig else 'No'}"
            )
        print(
            f"\nNote: significance level of {self.alpha} is used to determine whether the results are significant.\n"
        )
        print("----------------------------------\n")

def main():
    # Define paths and create folders
    project_dir = os.getcwd()
    raw_data_dir = os.path.join(project_dir, "data", "raw", "1")

    # Check if data folder exists
    if not os.path.exists(raw_data_dir):
        raise FileNotFoundError(
            f"Data folder does not exist at {raw_data_dir}. Please make sure you have downloaded the data by running download_data.py"
        )

    # Initialize analyzer
    analyzer = ABTestAnalyzer(raw_data_dir)

    # Specify the metrics to analyze and visualize
    metrics_to_analyze = [
        "spend",
        "reach",
        "impressions",
        "click_through_rate",
        "conversion_rate",
    ]

    # Perform and Visualize analysis
    analyzer.visualize_data(metrics_to_analyze)

    # Generate report of results
    analyzer.report_results(metrics_to_analyze)


if __name__ == "__main__":
    main()