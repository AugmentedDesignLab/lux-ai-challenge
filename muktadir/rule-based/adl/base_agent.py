from lux.kit import obs_to_game_state, GameState, EnvConfig
from lux.utils import direction_to, my_turn_to_place_factory
import numpy as np
import sys
import logging
class BaseAgent():
    def __init__(self, player: str, env_cfg: EnvConfig) -> None:
        self.player = player
        self.opp_player = "player_1" if self.player == "player_0" else "player_0"
        np.random.seed(0)
        self.env_cfg: EnvConfig = env_cfg
        self.logger = logging.getLogger(self.player)

    def debug(self, msg):
        self.logger.debug(msg)

    #region early setup methods
    def factoriesToPlace(self, game_state: GameState):
        return game_state.teams[self.player].factories_to_place
    
    def isMyTurn(self, game_state: GameState, step: int) -> bool:
        """Only called during the early_setup when agents take bidding/factory placement actions in turns.

        Args:
            game_state (GameState): _description_
            step (int): _description_

        Returns:
            bool: _description_
        """
        if game_state.teams[self.player].place_first:
            if step % 2 == 1:
                return True
        else:
            if step % 2 == 0:
                return True
        return False
    
    #endregion
