import numpy as np
from lux.kit import Board, GameState
from adl.utils import Utils
class BoardAnalyzer:

    
    def totalFactories(self, board: Board) -> int:
        return len(np.unique(board.factory_occupancy_map)) - 1

    def totalTiles(self, board: Board) -> int:
        return board.rubble.shape[0] * board.rubble.shape[1]
    
    def getFactoryBinaryOccupancy(self, board: Board) -> np.array:
        return board.factory_occupancy_map > -1

    def getGrowableTiles(self, board: Board, subtractRubbles=False) -> int:
        
        occupied = np.logical_or(board.ice, board.ore)
        occupied = np.logical_or(occupied, self.getFactoryBinaryOccupancy(board)) # or we can just subtract totalFactories

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

        waterProductionRate = Utils.getMaxWaterProductionRatePerFactory(game_state)
        factoryCapacity = self.totalFactories(board) * Utils.waterProductionRateToLichen(game_state, waterProductionRate)

        # print(self.totalFactories(board), growableTiles, factoryCapacity)

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

        waterProductionRate = Utils.getMaxWaterProductionRatePerFactory(game_state)
        factoryCapacity = len(game_state.factories[player]) * Utils.waterProductionRateToLichen(game_state, waterProductionRate)

        return min(growableTiles, factoryCapacity)




    

