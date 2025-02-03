import pandas as pd
from scipy import stats


class StatsUtils:
    """
    A class for performing statistical calculations on A/B test data.
    """

    def calculate_conversion_rate(
        self, data: pd.DataFrame, group_col: str, outcome_col: str
    ) -> pd.DataFrame:
        """Calculates conversion rate for each group."""
        conversion_rates = data.groupby(group_col)[outcome_col].mean().reset_index()
        conversion_rates.rename(columns={outcome_col: "conversion_rate"}, inplace=True)
        return conversion_rates

    def calculate_confidence_interval(
        self,
        data: pd.DataFrame,
        group_col: str,
        outcome_col: str,
        confidence: float = 0.95,
    ) -> pd.DataFrame:
        """Calculate a confidence interval for a binomial proportion (conversion rate).
        Args:
            data: the dataframe to calculate the CI.
            group_col: the name of the column that has the group information
            outcome_col: the column name that has the outcome of the experiment
            confidence: the confidence level

        Returns:
            The Dataframe with the results
        """

        # calculate the number of successes (conversions) and trials (sample size) for each group
        successes = data.groupby(group_col)[outcome_col].sum()
        trials = data.groupby(group_col)[outcome_col].count()
        # calculate the proportion (conversion rate) for each group
        proportions = successes / trials

        # calculate the standard error for each proportion
        standard_errors = (proportions * (1 - proportions) / trials).apply(
            lambda x: x**0.5
        )
        # calculate the critical value for the desired confidence level
        critical_value = stats.norm.ppf((1 + confidence) / 2)

        # calculate the margin of error for each proportion
        margin_of_errors = standard_errors * critical_value

        # calculate the confidence intervals for each proportion
        lower_bounds = proportions - margin_of_errors
        upper_bounds = proportions + margin_of_errors

        # create a DataFrame with the results
        results_df = pd.DataFrame(
            {
                "sample_size": trials,
                "successes": successes,
                "conversion_rate": proportions,
                "lower_bound": lower_bounds,
                "upper_bound": upper_bounds,
            }
        )
        results_df.reset_index(inplace=True)
        return results_df

    def perform_hypothesis_test(
        self, data: pd.DataFrame, group_col: str, outcome_col: str, alpha: float = 0.05
    ) -> tuple:
        """
        Performs a two-sample t-test to compare conversion rates between groups.
        """
        group_a = data[data[group_col] == "ad"][outcome_col]
        group_b = data[data[group_col] == "psa"][outcome_col]

        t_statistic, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
        return t_statistic, p_value, p_value < alpha
