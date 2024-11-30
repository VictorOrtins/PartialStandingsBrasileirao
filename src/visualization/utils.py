import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(project_path)

from src.calculations.corr import spearman_corr, normalized_tau_distance  # noqa: E402
from src.calculations.utils import spearman_tau_table


def positions_visualization(
    year_table: pd.DataFrame,
    line_width: float = 0.9,
    fig_size: tuple = (14, 8),
    colors: list = None,
):
    """
    Visualizes the positions of clubs throughout a season, showing how the rankings change over the matchweeks.

    Parameters:
        year_table (pd.DataFrame): The table with club rankings over different matchweeks.
        line_width (float, optional): The width of the lines in the plot. Default is 0.9.
        fig_size (tuple, optional): The size of the figure. Default is (14, 8).
        colors (list, optional): List of colors to use for the plot. If None, default colors are used.

    Returns:
        None: Displays a plot of the rankings over time.
    """
    if colors is None:
        colors = [
            "red",
            "blue",
            "green",
            "orange",
            "purple",
            "brown",
            "pink",
            "gray",
            "olive",
            "cyan",
            "magenta",
            "teal",
            "gold",
            "lime",
            "navy",
            "maroon",
            "violet",
            "turquoise",
            "indigo",
            "salmon",
        ]

    plt.figure(figsize=fig_size)

    for index, row in year_table.iterrows():
        x = year_table.columns.to_list()[:-1]
        y = row.to_list()[:-1]
        plt.plot(x, y, color=colors[index], linewidth=line_width)

    plt.xticks(ticks=[9, 19, 29], rotation=90)
    plt.yticks(ticks=[i for i in range(1, 21)], labels=year_table["Club"].to_list())

    plt.gca().invert_yaxis()

    ax = plt.gca()
    ax_right = ax.twinx()  # Criar um eixo Y adicional no lado direito
    ax_right.set_ylim(
        ax.get_ylim()
    )  # Sincronizar os limites do eixo direito com o esquerdo
    ax_right.set_yticks([20, 15, 10, 5, 1])  # Mesmos ticks do eixo esquerdo

    ax_right.set_label("Posição")
    plt.xlabel("Rodada")

    plt.show()


def spearman_tau_visualization(
    year_table: pd.DataFrame,
    line_width: float = 0.9,
    fig_size: tuple = (14, 8),
    colors: list = None,
    plot_points: tuple = None
):
    """
    Visualizes the Spearman correlation and normalized Kendall-tau distance for each matchweek.

    Parameters:
        year_table (pd.DataFrame): The table containing club rankings over different matchweeks.
        line_width (float, optional): The width of the lines in the plot. Default is 0.9.
        fig_size (tuple, optional): The size of the figure. Default is (14, 8).
        colors (list, optional): List of colors to use for the plot. If None, default colors are used.
        plot_points (tuple, optional): A tuple containing the Spearman correlation and Tau distance values. 
            If None, they will be computed using `spearman_tau_table`.

    Returns:
        None: Displays a plot of Spearman correlation and normalized Kendall-tau distance.
    """
    if colors is None:
        colors = ["orange", "black"]

    if plot_points is None:
        plot_points_corr, plot_points_tau = spearman_tau_table(year_table, return_as_list=True)
    else:
        plot_points_corr, plot_points_tau = plot_points[0], plot_points[1]

    x = [i for i in range(1, 39)]
    y = plot_points_corr

    plt.figure(figsize=fig_size)

    plt.yticks(ticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.ylim((-0.1, 1.1))

    plt.axhline(y=1.0, color="red", linestyle="--", linewidth=line_width).set_dashes(
        [10, 5]
    )
    plt.axhline(y=0.0, color="red", linestyle="--", linewidth=line_width).set_dashes(
        [10, 5]
    )

    plt.xticks(ticks=[10, 20, 30])
    plt.plot(x, y, label="Correlação de Spearman", color=colors[0])

    x = [i for i in range(1, 39)]
    y = plot_points_tau

    plt.plot(x, y, label="Distância de tau normalizada", color=colors[1])

    plt.legend()
    plt.show()

def tau_visualization(plot_points_list: list, labels: list, line_width: float = 0.9, fig_size: tuple = (14,8), colors: list = None):
    """
    Visualizes the normalized Kendall-tau distances for multiple series of rankings, comparing their changes over time.

    Parameters:
        plot_points_list (list): A list of data series to be plotted.
        labels (list): Labels for the plot series.
        line_width (float, optional): The width of the lines in the plot. Default is 0.9.
        fig_size (tuple, optional): The size of the figure. Default is (14, 8).
        colors (list, optional): List of colors to use for the plot. If None, colors are generated automatically.

    Returns:
        None: Displays a plot of multiple series of Tau distances.
    """
    if colors is None:
        num_colors = len(plot_points_list)
        cmap = plt.cm.get_cmap("tab10")  # Usando a paleta "tab10", mas pode ser qualquer outra
        colors = [cmap(i / num_colors) for i in range(num_colors)]  # Gera cores suficientes
    
    if len(plot_points_list) != len(labels) or len(labels) != len(colors):
        return None
    
    plt.figure(figsize=fig_size)

    for plot_points, label, color in zip(plot_points_list, labels, colors):
        plt.yticks(ticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        plt.ylim((-0.1, 1.1))

        plt.axhline(y=1.0, color="red", linestyle="--", linewidth=line_width).set_dashes(
            [10, 5]
        )
        plt.axhline(y=0.0, color="red", linestyle="--", linewidth=line_width).set_dashes(
            [10, 5]
        )
        plt.xticks(ticks=[10, 20, 30])

        x = [i for i in range(1, len(plot_points) + 1)]
        y = plot_points
        plt.plot(x, y, label=label, color=color)

    plt.legend()
    plt.show()



    

