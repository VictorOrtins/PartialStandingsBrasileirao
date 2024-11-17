import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

project_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(project_path)

from src.calculations.utils import spearman_corr, normalized_tau_distance

def positions_visualization(year_table: pd.DataFrame, line_width: float = 0.9, fig_size: tuple = (14,8), colors: list = None):
    if colors is None:
        colors = [
            "red", "blue", "green", "orange", "purple", "brown", "pink", "gray", 
            "olive", "cyan", "magenta", "teal", "gold", "lime", "navy", "maroon", 
            "violet", "turquoise", "indigo", "salmon"
        ]

    plt.figure(figsize=fig_size)

    for index, row in year_table.iterrows():
        x = year_table.columns.to_list()[:-1]
        y = row.to_list()[:-1]
        plt.plot(x, y, color=colors[index], linewidth=line_width)


    plt.xticks(ticks=[9, 19, 29], rotation=90)
    plt.yticks(ticks=[i for i in range(1, 21)], labels=year_table['Club'].to_list())

    plt.gca().invert_yaxis()


    ax = plt.gca()
    ax_right = ax.twinx()  # Criar um eixo Y adicional no lado direito
    ax_right.set_ylim(ax.get_ylim())  # Sincronizar os limites do eixo direito com o esquerdo
    ax_right.set_yticks([20, 15, 10, 5, 1])  # Mesmos ticks do eixo esquerdo

    ax_right.set_label('Posição')
    plt.xlabel('Rodada')


    plt.show()

def spearman_tau_visualization(year_table: pd.DataFrame, line_width: float = 0.9, fig_size: tuple = (14,8), colors: list = None):
    if colors is None:
        colors = ['orange', 'black']
    
    plot_points_corr = []
    plot_points_tau = []

    for i in range(1, 39):
        rho, _ = spearman_corr(year_table[f'{i}'].to_list(), year_table['38'].to_list())
        plot_points_corr.append(rho)

        norm_tau_distance = normalized_tau_distance(year_table[f'{i}'].to_list(), year_table['38'].to_list())
        plot_points_tau.append(norm_tau_distance)

    x = [i for i in range(1, 39)]
    y = plot_points_corr

    plt.figure(figsize=fig_size)

    plt.yticks(ticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.ylim((-0.1, 1.1))

    plt.axhline(y=1.0, color='red', linestyle='--', linewidth=line_width).set_dashes([10,5])
    plt.axhline(y=0.0, color='red', linestyle='--', linewidth=line_width).set_dashes([10,5])

    plt.xticks(ticks=[10, 20, 30])
    plt.plot(x, y, label="Correlação de Spearman")

    x = [i for i in range(1, 39)]
    y = plot_points_tau

    plt.plot(x, y, label="Distância de tau normalizada")

    plt.legend()
    plt.show()