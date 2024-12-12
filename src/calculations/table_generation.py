import numpy as np
import pandas as pd

from typing import List, Tuple

def init_standings(n_teams: int = 20, random_seed: int = 42):
    np.random.seed(random_seed)

    team_names = list(range(0, n_teams))

    standings = pd.DataFrame(
        {
            "Club": team_names,
            "Pts": 0,
            "Matches": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "+": 0,
            "-": 0,
            "SG": 0,
            "Position": 0,
        }
    )

    rank_table_df = pd.DataFrame(columns=[f"{i}" for i in range(1, 39)])

    return rank_table_df, standings

def update_goals_from_match(standings: pd.DataFrame, match: Tuple[int, int], goals_a: int, goals_b: int):
    standings.loc[match[0], "Matches"] += 1
    standings.loc[match[1], "Matches"] += 1

    standings.loc[match[0], "+"] += goals_a
    standings.loc[match[1], "+"] += goals_b

    standings.loc[match[0], "-"] += goals_b
    standings.loc[match[1], "-"] += goals_a

    standings.loc[match[0], "SG"] += goals_a - goals_b
    standings.loc[match[1], "SG"] += goals_b - goals_a

    return standings

def update_table(standings: pd.DataFrame, match: Tuple[int, int], goals_a: int, goals_b: int):
    if goals_a > goals_b:
        standings.loc[match[0], "W"] += 1
        standings.loc[match[1], "L"] += 1
        standings.loc[match[0], "Pts"] += 3
    elif goals_a < goals_b:
        standings.loc[match[1], "W"] += 1
        standings.loc[match[0], "L"] += 1
        standings.loc[match[1], "Pts"] += 3
    else:
        standings.loc[match[0], "D"] += 1
        standings.loc[match[1], "D"] += 1
        standings.loc[match[0], "Pts"] += 1
        standings.loc[match[1], "Pts"] += 1

    return standings

def set_table_positions(standings: pd.DataFrame):
    standings = standings.sort_values(by=["Pts", "SG", "+"], ascending=False)
    position = 1
    for _, row in standings.iterrows():
        row["Position"] = position
        position += 1

    return standings

def update_rank_table(rank_table_df: pd.DataFrame, standings:pd.DataFrame, matchweek: int):
    if matchweek == 0:
        clubs = standings["Club"]
        for index, club in enumerate(clubs):
            rank_table_df.at[index, "Club"] = int(club)
            rank_table_df.at[index, f"{matchweek + 1}"] = index + 1
    else:
        for index, row in standings.iterrows():
            club = row["Club"]

            club_index = rank_table_df[rank_table_df["Club"] == club].index
            club_index = club_index.item()
            rank_table_df.at[club_index, f"{matchweek + 1}"] = int(
                row["Position"]
            )

    return rank_table_df, standings


def generate_table(
    poisson_mean: float, n_teams: int = 20, random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates a table of football standings by simulating match results over a season.

    Parameters:
        poisson_mean (float): The mean of the Poisson distribution for simulating match goals.
        n_teams (int, optional): The number of teams in the league. Default is 20.
        random_seed (int, optional): The seed for the random number generator. Default is 42.

    Returns:
        pd.DataFrame: A dataframe containing the standings with the club positions after each matchweek.
    """

    rank_table_df, standings = init_standings(n_teams, random_seed)

    fixtures = generate_matchweeks(n_teams)

    for matchweek_i, matchweek in enumerate(fixtures):
        for match in matchweek:
            goals_a, goals_b = simulate_match(poisson_mean)

            standings = update_goals_from_match(standings, match, goals_a, goals_b)
            standings = update_table(standings, match, goals_a, goals_b)

        standings = set_table_positions(standings)

        rank_table_df, standings = update_rank_table(rank_table_df, standings, matchweek_i)


    return rank_table_df


def simulate_match(poisson_mean: float) -> Tuple[float, float]:
    """
    Simulates the result of a football match based on a Poisson distribution.

    Parameters:
        poisson_mean (float): The mean number of goals scored in a match.

    Returns:
        tuple: A tuple containing the goals scored by the home team and away team.
    """

    goals_a = np.random.poisson(poisson_mean)
    goals_b = np.random.poisson(poisson_mean)

    return goals_a, goals_b


def generate_matchweeks(n_teams: int = 20) -> List[List[Tuple[int, int]]]:
    """
    Generates matchweeks for a round-robin league with home and away fixtures.

    Parameters:
        n_teams (int, optional): The number of teams in the league. Must be even. Default is 20.

    Returns:
        list of lists: A list of rounds, where each round contains a list of matchups.

    Raises:
        Exception: If the number of teams is odd, an exception will be raised.
    """

    if n_teams % 2 == 1:
        raise Exception("Number of teams must be even")

    teams = list(range(0, n_teams))
    anchor = teams[0]
    rotating_teams = teams[1:]

    first_legs = []
    for _ in range(n_teams - 1):
        round_matches = []
        for j in range(len(rotating_teams) // 2):
            home = rotating_teams[j]
            away = rotating_teams[-(j + 1)]
            round_matches.append((home, away))

        round_matches.append((anchor, rotating_teams[len(rotating_teams) // 2]))

        first_legs.append(round_matches)

        rotating_teams = [rotating_teams[-1]] + rotating_teams[:-1]

    second_legs = []
    for round in first_legs:
        new_round = [(match[1], match[0]) for match in round]
        second_legs.append(new_round)

    rounds = first_legs + second_legs

    return rounds
