import os
import sys

import pandas as pd

from typing import List, Tuple

project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_path)

from src.calculations.corr import spearman_corr, normalized_tau_distance  # noqa: E402
from src.calculations.table_generation import generate_table  # noqa: E402


def get_plot_points(year_table: pd.DataFrame, matchweek: int, plot_points_corr: List[float], plot_points_tau: List[float]):
    rho, _ = spearman_corr(year_table[f"{matchweek}"].to_list(), year_table["38"].to_list())
    plot_points_corr.append(rho)

    norm_tau_distance: float = normalized_tau_distance(
        year_table[f"{matchweek}"].to_list(), year_table["38"].to_list()
    )
    plot_points_tau.append(norm_tau_distance)

    return plot_points_corr, plot_points_tau

def spearman_tau_table(
    year_table: pd.DataFrame, return_as_list: bool = False
) -> pd.DataFrame:
    """
    Computes the Spearman correlation and normalized Kendall-tau distance for a given season's rankings.

    Parameters:
        year_table (pd.DataFrame): The table containing the rankings of teams over different matchweeks.
        return_as_list (bool, optional): If True, returns the results as lists;
            otherwise, returns them as a DataFrame. Default is False.

    Returns:
        pd.DataFrame or tuple: The Spearman correlations and normalized Kendall-tau distances either as a DataFrame
            or as separate lists, based on the `return_as_list` flag.
    """

    plot_points_corr: List[float] = []
    plot_points_tau: List[float] = []

    for i in range(1, 39):
        plot_points_corr, plot_points_tau = get_plot_points(year_table, i, plot_points_corr, plot_points_tau)

    if return_as_list:
        return plot_points_corr, plot_points_tau

    table_df: pd.DataFrame = pd.DataFrame(
        [plot_points_corr, plot_points_tau],
        columns=[i for i in range(1, 39)],
        index=["Spearman", "Tau"],
    )

    return table_df


def generate_spearman_tau(num_seasons: int = 22) -> Tuple[List[float], List[float]]:
    """
    Generates the average Spearman correlation and normalized Kendall-tau distance over a number of seasons.

    Parameters:
        num_seasons (int, optional): The number of seasons to simulate. Default is 22.

    Returns:
        tuple: The mean Spearman correlation and mean normalized Kendall-tau distance across all simulated seasons.
    """
    spearmans_list: List[List[float]] = []
    taus_list: List[List[float]] = []

    for i in range(1, num_seasons + 1):
        rank_table_df: pd.DataFrame = generate_table(1.325, random_seed=i)
        spearman_list, tau_list = spearman_tau_table(rank_table_df, return_as_list=True)

        spearmans_list.append(spearman_list)
        taus_list.append(tau_list)

    return spearman_tau_mean(taus_list, spearmans_list)


def spearman_tau_from_tables(years_table_list: list) -> Tuple[List[float], List[float]]:
    """
    Computes the average Spearman correlation and normalized Kendall-tau distance from a list of ranking tables.

    Parameters:
        years_table_list (list): A list of ranking tables, one for each season.

    Returns:
        tuple: The mean Spearman correlation and mean normalized Kendall-tau distance across all seasons.
    """
    spearmans_list: List[List[float]] = []
    taus_list: List[List[float]] = []

    for rank_table_df in years_table_list:
        spearman_list, tau_list = spearman_tau_table(rank_table_df, return_as_list=True)

        spearmans_list.append(spearman_list)
        taus_list.append(tau_list)

    return spearman_tau_mean(taus_list, spearmans_list)


def spearman_tau_mean(
    taus_list: list, spearmans_list: list
) -> Tuple[List[float], List[float]]:
    """
    Calculates the mean Spearman correlation and mean normalized Kendall-tau distance from multiple seasons.

    Parameters:
        taus_list (list): A list of normalized Kendall-tau distances for each season.
        spearmans_list (list): A list of Spearman correlation coefficients for each season.

    Returns:
        tuple: The mean Spearman correlation and the mean normalized Kendall-tau distance across all seasons.
    """

    if len(taus_list) != len(spearmans_list):
        return None

    sum_spearmans_list: List[int] = [0] * len(spearmans_list[0])
    sum_taus_list: List[int] = [0] * len(taus_list[0])

    for i in range(0, len(spearmans_list[0])):
        for spearman_list, tau_list in zip(spearmans_list, taus_list):
            sum_spearmans_list[i] += spearman_list[i]
            sum_taus_list[i] += tau_list[i]

    mean_spearmans_list: List[float] = [sum_num / (len(taus_list)) for sum_num in sum_spearmans_list]
    mean_taus_list: List[float] = [sum_num / (len(taus_list)) for sum_num in sum_taus_list]

    return mean_spearmans_list, mean_taus_list
