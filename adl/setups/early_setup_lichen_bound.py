import numpy as np
from lux.kit import obs_to_game_state, GameState, EnvConfig, Team
from ..utils import *
from adl.base_agent import BaseAgent
from ..utils import Utils

def early_setup_lichen_bound(self: BaseAgent, step: int, obs, remainingOverageTime: int = 60):

    
    game_state = obs_to_game_state(step, self.env_cfg, obs)

    if step == 0:
        print("maxFactoriesPerPlayer", game_state.maxFactoriesPerPlayer)
        # bid 0 to not waste resources bidding and declare as the default faction
        return dict(faction="AlphaStrike", bid=0)
    else:


        # factory placement period

        # how much water and metal you have in your starting pool to give to new factories
        water_left = game_state.teams[self.player].water
        metal_left = game_state.teams[self.player].metal


        if self.isMyTurn(game_state, step) and self.factoriesToPlace(game_state) > 0:

            self.logger.info(f"{self.player} has {water_left} water and {metal_left} metal")
            self.logger.info(f"Early Setup: lichen UB before bidding: {self.boardAnalyzer.getLichenUBBeforeBidding(game_state)}")
            self.logger.info(f"Early Setup:  lichen UB after bidding: {self.boardAnalyzer.getLichenUBAfterAfterBidding(game_state)}")

            self.cacheInvariants(game_state)

            # decide how many factories we need
            
            maxLichensICanGrow = self.boardAnalyzer.getLichenUBBeforeBidding(game_state) // 2
            maxFactoriesICanHave = game_state.maxFactoriesPerPlayer

            targetLichens = min(maxLichensICanGrow, Utils.factoryToLichen(game_state, game_state.maxFactoriesPerPlayer))

            factoriesNeeded = targetLichens // Utils.factoryToLichen(game_state, 1)

            self.logger.info(f"{self.player} exiting factories {len(game_state.factories[self.player])}")

            print("maxFactoriesPerPlayer", game_state.maxFactoriesPerPlayer)
            print("targetLichens", targetLichens)
            print("lichenPerFactory", Utils.factoryToLichen(game_state, 1))
            print("factoriesNeeded", factoriesNeeded)

            totalWater = game_state.env_cfg.INIT_WATER_METAL_PER_FACTORY * game_state.maxFactoriesPerPlayer

            # we only spawn as many factories as we need, not all.
            resourcePerFactory = totalWater // factoriesNeeded
            
            # is this the last one we are placing
            if self.factoriesToPlace == 1:
                resourcePerFactory = water_left

            print("resourcePerFactory", resourcePerFactory)

            # we will spawn our factory in a random location with 150 metal and water if it is our turn to place
            potential_spawns = Utils.get_potential_spawns(obs)
            print("potential spawn", len(potential_spawns))
            spawn_loc = potential_spawns[np.random.randint(0, len(potential_spawns))]
            # self.logger.info(f"Early Setup:  lichen UB {self.player}: {self.boardAnalyzer.getLichenUBAfterAfterBiddingByPlayer(self.player, game_state)}")
            return dict(spawn=spawn_loc, metal=resourcePerFactory, water=resourcePerFactory)
            # return dict(spawn=spawn_loc, metal=150, water=150)
    
    return dict()