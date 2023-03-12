import numpy as np
import math
from lux.kit import Board, GameState
from adl.utils import Utils
class BoardAnalyzer:

    
    def totalFactoriesPlaced(self, board: Board) -> int:
        return len(np.unique(board.factory_occupancy_map)) - 1

    def totalTiles(self, board: Board) -> int:
        return board.rubble.shape[0] * board.rubble.shape[1]
    
    def getFactoryBinaryOccupancy(self, board: Board) -> np.array:
        return board.factory_occupancy_map > -1

    def getGrowableTiles(self, board: Board, subtractRubbles=False) -> int:
        
        occupied = np.logical_or(board.ice, board.ore)
        occupied = np.logical_or(occupied, self.getFactoryBinaryOccupancy(board)) # or we can just subtract totalFactoriesPlaced

        if subtractRubbles:
            occupied = np.logical_or(occupied, board.rubble)
        
        return self.totalTiles(board) - np.sum(occupied)


    def getLichenUBBeforeBidding(self, game_state: GameState, subtractRubbles=False) -> int:
        """Returns the maximum # lichens based on the maximum number of factories by both players and the number of available growable tiles

        Args:
            game_state (GameState): _description_
            subtractRubbles (bool, optional): _description_. Defaults to False.

        Returns:
            int: _description_
        """
        
        board = game_state.board

        growableTiles = self.getGrowableTiles(board)

        waterProductionRate = Utils.getMaxWaterProductionRatePerFactory(game_state)
        factoryCapacity = board.factories_per_team * 2 * Utils.waterProductionRateToLichen(game_state, waterProductionRate)
        factoryCapacity = Utils.factoryToLichen(game_state, board.factories_per_team * 2)

        # print(board.factories_per_team * 2, growableTiles, factoryCapacity)

        return min(growableTiles, factoryCapacity)
    
    def getLichenUBAfterAfterBidding(self, game_state: GameState, subtractRubbles=False) -> int:
        """Returns the maximum # lichens based on the number of all the factories placed so far by both players and the number of available growable tiles

        Args:
            game_state (GameState): _description_
            subtractRubbles (bool, optional): _description_. Defaults to False.

        Returns:
            int: _description_
        """
        
        board = game_state.board
        
        growableTiles = self.getGrowableTiles(board)

        factoryCapacity = Utils.factoryToLichen(game_state, self.totalFactoriesPlaced(board))

        return min(growableTiles, factoryCapacity)
    
    def getLichenUBAfterAfterBiddingByPlayer(self, player: str, game_state: GameState, subtractRubbles=False) -> int:
        """Returns the maximum # lichens based on the number of factories the player has and the number of available growable tiles

        Args:
            player (str): _description_
            game_state (GameState): _description_
            subtractRubbles (bool, optional): _description_. Defaults to False.

        Returns:
            int: _description_
        """

        board = game_state.board
        growableTiles = self.getGrowableTiles(board)

        factoryCapacity = Utils.factoryToLichen(game_state, len(game_state.factories[player]))

        return min(growableTiles, factoryCapacity)

    
    def idealDiameter(self, game_state: GameState) -> int:
        """
        returns a radius for ideal localion of ice/ore.
        """
        maxLichenPerFactory = Utils.factoryToLichen(game_state, 1)
        return int(math.sqrt(maxLichenPerFactory - 9)) # 9 for factory area




    

