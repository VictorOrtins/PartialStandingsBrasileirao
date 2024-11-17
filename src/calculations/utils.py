from scipy.stats import spearmanr
from scipy.stats import kendalltau

def spearman_corr(partial_standings, final_standings, alternative='two-sided'):
    corr, p_value = spearmanr(partial_standings, final_standings, alternative=alternative)
    return corr, p_value

def normalized_tau_distance(partial_standings, final_standings, complete_return: bool = False):
    tau_corr, _ = kendalltau(partial_standings, final_standings)
    tau_distance = ((1 - tau_corr)*(len(partial_standings)*(len(partial_standings) - 1)))/4
    normalized_tau_distance = 2*tau_distance/(len(partial_standings)*(len(partial_standings) - 1))

    if complete_return:
        return normalized_tau_distance, tau_distance, tau_corr
    
    return normalized_tau_distance