import pandas as pd

### FAZER EXEMPLO NA MÃO PRA CONFERIR RESULTADOS!!!

def calculate_transitions_year(
    rank_table_df: pd.DataFrame,
    transition_table_df: pd.DataFrame,
    init_round: int = 10,
    final_round: int = 38,
):
    init_round_standings = rank_table_df[f"{init_round}"]
    final_round_standings = rank_table_df[f"{final_round}"]

    for index, init_round_standing in init_round_standings.items():
        final_round_standing = final_round_standings.loc[index]
        transition_table_df.at[init_round_standing, final_round_standing] += 1

    return transition_table_df


def calculate_transitions_history(
    rank_tables_list: list, init_round: int = 10, final_round: int = 38
):
    transition_table_df = pd.DataFrame(
        0, columns=[i for i in range(1, 21)], index=[i for i in range(1, 21)]
    )

    for rank_table_df in rank_tables_list:
        transition_table_df = calculate_transitions_year(rank_table_df, transition_table_df, init_round, final_round)

    transition_table_df = transition_table_df.apply(lambda x: x / len(rank_tables_list))
    
    return transition_table_df

