from adl.board_analysis import BoardAnalyzer
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


        self.boardAnalyzer = BoardAnalyzer()

        # these props can only be read after setup
        self._ice_locations: np.ndarray = None
        self._ore_locations: np.ndarray = None

    def debug(self, msg):
        self.logger.debug(msg)
        
    @property
    def iceLocations(self):
        return self._ice_locations
        
    @property
    def oreLocations(self):
        return self._ore_locations

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


    def cacheInvariants(self, game_state: GameState):
        self._ice_locations = np.argwhere(game_state.board.ice == 1)
        self._ore_locations = np.argwhere(game_state.board.ore == 1)
        # distance to ice and ore from factory is fixed


    def distanceToIceLocations(self, fromPos:np.ndarray) -> np.ndarray:
        return np.mean((self.iceLocations - fromPos) ** 2, 1)
    
    def closestIceFrom(self, fromPos:np.ndarray) -> np.ndarray:
        return self.iceLocations[np.argmin(self.distanceToIceLocations(fromPos))]

    def distanceToOreLocations(self, fromPos:np.ndarray) -> np.ndarray:
        return np.mean((self.oreLocations - fromPos) ** 2, 1)
    
    def closestOreFrom(self, fromPos:np.ndarray) -> np.ndarray:
        return self.oreLocations[np.argmin(self.distanceToOreLocations(fromPos))]
    
    
    #endregion
