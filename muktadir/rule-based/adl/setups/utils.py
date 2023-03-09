import numpy as np

def get_potential_spawns(obs):
    return np.array(list(zip(*np.where(obs["board"]["valid_spawns_mask"] == 1))))