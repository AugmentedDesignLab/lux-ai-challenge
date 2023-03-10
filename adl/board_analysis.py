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
    
    def getLichenUBBeforeFactoryPlacement(self, game_state: GameState, subtractRubbles=False) -> int:
        
        board = game_state.board

        occupied = np.logical_or(board.ice, board.ore)
        occupied = np.logical_or(occupied, self.getFactoryBinaryOccupancy(board)) # or we can just subtract totalFactories

        if subtractRubbles:
            occupied = np.logical_or(occupied, board.rubble)
        
        growableTiles = self.totalTiles(board) - np.sum(occupied)

        waterProductionRate = Utils.getMaxWaterProductionRatePerFactory(game_state)


        factoryCapacity = board.factories_per_team * 2 * (waterProductionRate -1) * game_state.env_cfg.LICHEN_WATERING_COST_FACTOR

        print(board.factories_per_team * 2, growableTiles, factoryCapacity)

        return min(growableTiles, factoryCapacity)
    
    def getLichenUBAfterFactoryPlacement(self, game_state: GameState, subtractRubbles=False) -> int:
        
        board = game_state.board

        occupied = np.logical_or(board.ice, board.ore)
        occupied = np.logical_or(occupied, self.getFactoryBinaryOccupancy(board)) # or we can just subtract totalFactories

        if subtractRubbles:
            occupied = np.logical_or(occupied, board.rubble)
        
        growableTiles = self.totalTiles(board) - np.sum(occupied)

        waterProductionRate = Utils.getMaxWaterProductionRatePerFactory(game_state)


        factoryCapacity = self.totalFactories(board) * (waterProductionRate -1) * game_state.env_cfg.LICHEN_WATERING_COST_FACTOR

        print(self.totalFactories(board), growableTiles, factoryCapacity)

        return min(growableTiles, factoryCapacity)



    

