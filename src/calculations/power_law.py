from typing import List


class TauPowerLaw:
    """
    A class representing a power law function to model Kendall-tau distance
    as a function of the round number.

    Attributes:
        a (float): The power coefficient (exponent) in the power law.
        b (float): The multiplier coefficient in the power law.

    Methods:
        tau_distance(round):
            Computes the Kendall-tau distance for a given round using the power law formula.

        taus_distances(init_round, end_round):
            Computes the Kendall-tau distances for a range of rounds from `init_round` to `end_round`.
    """

    def __init__(self, power_coefficient: float, multiplier_coefficient: float):
        """
        Initializes the TauPowerLaw instance with the given power and multiplier coefficients.

        Parameters:
            power_coefficient (float): The exponent coefficient for the power law.
            multiplier_coefficient (float): The multiplier coefficient for the power law.
        """
        self.a = power_coefficient
        self.b = multiplier_coefficient

    def tau_distance(self, round: int) -> float:
        """
        Computes the Kendall-tau distance for a specific round using the power law formula.

        Parameters:
            round (int): The round number for which to compute the Kendall-tau distance.

        Returns:
            float: The computed Kendall-tau distance for the given round.
        """
        return self.b * round**self.a

    def taus_distances(self, init_round: int, end_round: int) -> List[float]:
        """
        Computes the Kendall-tau distances for a range of rounds from `init_round` to `end_round`.

        Parameters:
            init_round (int): The starting round.
            end_round (int): The ending round.

        Returns:
            list of float: A list of Kendall-tau distances for each round in the given range.
        """
        return [self.tau_distance(round) for round in range(init_round, end_round + 1)]
