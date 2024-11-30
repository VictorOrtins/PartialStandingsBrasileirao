from scipy.stats import spearmanr, kendalltau
from typing import List, Tuple, Union


def spearman_corr(
    partial_standings: List[int],
    final_standings: List[int],
    alternative: str = "two-sided",
) -> Tuple[float, float]:
    """
    Computes the Spearman correlation between two rankings and the associated p-value.

    Parameters:
        partial_standings (list or array-like): List of partial rankings.
        final_standings (list or array-like): List of final rankings.
        alternative (str, optional): Type of hypothesis test:
            - 'two-sided' (default): Two-tailed test.
            - 'less': Tests if the correlation is less than zero.
            - 'greater': Tests if the correlation is greater than zero.

    Returns:
        corr (float): Spearman correlation coefficient, between -1 and 1.
        p_value (float): p-value of the hypothesis test.
    """

    if len(partial_standings) != len(final_standings):
        raise ValueError(
            "Partial standings and final standings must have the same length"
        )

    corr, p_value = spearmanr(
        partial_standings, final_standings, alternative=alternative
    )
    return corr, p_value


def normalized_tau_distance(
    partial_standings: List[int], final_standings, complete_return: bool = False
) -> Union[float, Tuple[float, float, float]]:
    """
    Computes the normalized Kendall-tau distance between two rankings.

    Parameters:
        partial_standings (list or array-like): List of partial rankings.
        final_standings (list or array-like): List of final rankings.
        complete_return (bool, optional): If True, also returns the raw Kendall-tau distance
            and the Kendall-tau correlation. Default is False.

    Returns:
        If complete_return is False:
            normalized_tau_distance (float): Normalized Kendall-tau distance.
        If complete_return is True:
            normalized_tau_distance (float): Normalized Kendall-tau distance, between 0 and 1.
            tau_distance (float): Raw Kendall-tau distance.
            tau_corr (float): Kendall-tau correlation coefficient, between -1 and 1.
    """

    if len(partial_standings) != len(final_standings):
        raise ValueError(
            "Partial standings and final standings must have the same length"
        )

    tau_corr, _ = kendalltau(partial_standings, final_standings)
    tau_distance = (
        (1 - tau_corr) * (len(partial_standings) * (len(partial_standings) - 1))
    ) / 4
    normalized_tau_distance = (
        2 * tau_distance / (len(partial_standings) * (len(partial_standings) - 1))
    )

    if complete_return:
        return normalized_tau_distance, tau_distance, tau_corr

    return normalized_tau_distance
