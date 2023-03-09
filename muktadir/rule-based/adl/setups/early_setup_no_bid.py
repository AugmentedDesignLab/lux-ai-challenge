import numpy as np
from lux.kit import obs_to_game_state, GameState, EnvConfig, Team

def early_setup_no_bid(self, step: int, obs, remainingOverageTime: int = 60):
    if not self.isMyTurn(game_state, step):
        return dict()

    if step == 0:
        # bid 0 to not waste resources bidding and declare as the default faction
        return dict(faction="AlphaStrike", bid=0)
    else:
        game_state = obs_to_game_state(step, self.env_cfg, obs)
        # factory placement period

        # how much water and metal you have in your starting pool to give to new factories
        water_left = game_state.teams[self.player].water
        metal_left = game_state.teams[self.player].metal

        if self.factoriesToPlace > 0:
            # we will spawn our factory in a random location with 150 metal and water if it is our turn to place
            potential_spawns = np.array(list(zip(*np.where(obs["board"]["valid_spawns_mask"] == 1))))
            spawn_loc = potential_spawns[np.random.randint(0, len(potential_spawns))]
            return dict(spawn=spawn_loc, metal=150, water=150)
    
    return dict()