import numpy as np
from lux.kit import obs_to_game_state, GameState, EnvConfig, Team
from ..utils import *
from adl.base_agent import BaseAgent
from ..utils import Utils

def early_setup_no_bid(self: BaseAgent, step: int, obs, remainingOverageTime: int = 60):

    if step == 0:
        # bid 0 to not waste resources bidding and declare as the default faction
        return dict(faction="AlphaStrike", bid=0)
    else:
        game_state = obs_to_game_state(step, self.env_cfg, obs)
        # factory placement period

        # how much water and metal you have in your starting pool to give to new factories
        water_left = game_state.teams[self.player].water
        metal_left = game_state.teams[self.player].metal

        self.logger.info(f"{self.player} has {water_left} water and {metal_left} metal")

        if self.isMyTurn(game_state, step) and self.factoriesToPlace(game_state) > 0:
            self.cacheInvariants(game_state)
            # we will spawn our factory in a random location with 150 metal and water if it is our turn to place
            potential_spawns = Utils.get_potential_spawns(obs)
            spawn_loc = potential_spawns[np.random.randint(0, len(potential_spawns))]
            return dict(spawn=spawn_loc, metal=150, water=150)
    
    return dict()