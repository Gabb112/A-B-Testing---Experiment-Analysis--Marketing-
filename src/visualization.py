import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


class Visualization:
    """
    A class for creating visualizations for A/B testing results.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_conversion_rates(
        self,
        conversion_rates: pd.DataFrame,
        group_col: str,
        rate_col: str,
        filename: str = "conversion_rates.png",
    ):
        """Creates a bar chart of conversion rates."""
        plt.figure(figsize=(8, 6))
        sns.barplot(x=group_col, y=rate_col, data=conversion_rates)
        plt.title("Conversion Rates by Group")
        plt.ylabel("Conversion Rate")
        self.save_plot(filename)

    def plot_confidence_intervals(
        self,
        confidence_intervals: pd.DataFrame,
        group_col: str,
        filename: str = "confidence_intervals.png",
    ):
        """Creates a plot of the confidence intervals
        Args:
            confidence_intervals: Dataframe with the results. Must contain columns ['lower_bound', 'upper_bound', 'conversion_rate']
            group_col: name of the column that has the group name
            filename: name of the file where the figure will be saved.
        """

        plt.figure(figsize=(10, 6))

        for i in range(len(confidence_intervals)):
            group_name = confidence_intervals[group_col][i]
            conversion_rate = confidence_intervals["conversion_rate"][i]
            lower_bound = confidence_intervals["lower_bound"][i]
            upper_bound = confidence_intervals["upper_bound"][i]
            plt.errorbar(
                x=group_name,
                y=conversion_rate,
                yerr=[[conversion_rate - lower_bound], [upper_bound - conversion_rate]],
                fmt="o",
                capsize=5,
                label=f"{group_name} CI",
            )

        plt.xlabel("Groups")
        plt.ylabel("Conversion Rate with 95% CI")
        plt.title("Conversion Rate and 95% Confidence Intervals")
        plt.legend()
        self.save_plot(filename)

    def plot_feature_distributions(
        self,
        data: pd.DataFrame,
        feature_col: str,
        group_col: str,
        filename: str = "feature_distributions.png",
    ):
        """Plots the distribution of a numerical feature for each group"""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data, x=feature_col, hue=group_col, kde=True)
        plt.title(f"Distribution of '{feature_col}' by Group")
        plt.xlabel(feature_col)
        plt.ylabel("Frequency")
        self.save_plot(filename)

    def save_plot(self, filename: str):
        """Saves the current matplotlib plot to the specified file"""
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
