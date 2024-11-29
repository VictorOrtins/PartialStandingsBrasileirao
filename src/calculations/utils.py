import os
import sys

import pandas as pd

project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_path)

from src.calculations.corr import spearman_corr, normalized_tau_distance  # noqa: E402
from src.calculations.table_generation import generate_table  # noqa: E402


def spearman_tau_table(
    year_table: pd.DataFrame,
    return_as_list: bool = False
):

    plot_points_corr = []
    plot_points_tau = []

    for i in range(1, 39):
        rho, _ = spearman_corr(year_table[f"{i}"].to_list(), year_table["38"].to_list())
        plot_points_corr.append(rho)

        norm_tau_distance = normalized_tau_distance(
            year_table[f"{i}"].to_list(), year_table["38"].to_list()
        )
        plot_points_tau.append(norm_tau_distance)


    if return_as_list:
        return plot_points_corr, plot_points_tau
    
    table_df = pd.DataFrame([plot_points_corr, plot_points_tau], columns=[i for i in range(1, 39)], index=['Spearman', 'Tau'])

    return table_df

def generate_spearman_tau_22_seasons():
    spearmans_list = []
    taus_list = []

    for i in range(1, 23):
        rank_table_df = generate_table(1.325, random_seed=i)
        spearman_list, tau_list = spearman_tau_table(rank_table_df, return_as_list=True)

        spearmans_list.append(spearman_list)
        taus_list.append(tau_list)

    sum_spearmans_list = [0]*len(spearmans_list[0])
    sum_taus_list = [0]*len(taus_list[0])

    for i in range(0, len(spearmans_list[0])):
        for spearman_list, tau_list in zip(spearmans_list, taus_list):
            sum_spearmans_list[i] += spearman_list[i]
            sum_taus_list[i] += tau_list[i]

    mean_spearmans_list = [sum_num/22 for sum_num in sum_spearmans_list]
    mean_taus_list = [sum_num/22 for sum_num in sum_taus_list]

    return mean_spearmans_list, mean_taus_list