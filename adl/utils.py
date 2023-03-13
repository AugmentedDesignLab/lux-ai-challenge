import numpy as np

from lux.kit import GameState

class Utils:

    @staticmethod
    def get_potential_spawns(obs):
        return np.array(list(zip(*np.where(obs["board"]["valid_spawns_mask"] == 1))))

    @staticmethod
    def getMaxWaterProductionRatePerFactory(game_state: GameState) -> int:
        return game_state.env_cfg.FACTORY_PROCESSING_RATE_WATER / game_state.env_cfg.ICE_WATER_RATIO

    @staticmethod
    def getMaxMetalProductionRatePerFactory(game_state: GameState) -> int:
        return game_state.env_cfg.FACTORY_PROCESSING_RATE_METAL / game_state.env_cfg.ORE_METAL_RATIO
    
    @staticmethod
    def waterProductionRateToLichen(game_state: GameState, waterProductionRate: int) -> int:
        return (waterProductionRate -1) * game_state.env_cfg.LICHEN_WATERING_COST_FACTOR
    
    @staticmethod
    def factoryToLichen(game_state: GameState, nFactory: int) -> int:
        waterProductionRatePerFactory = Utils.getMaxWaterProductionRatePerFactory(game_state)
        return nFactory * Utils.waterProductionRateToLichen(game_state, waterProductionRatePerFactory)
    
    @staticmethod
    def distanceToLocations(locations: np.ndarray, fromPos:np.ndarray) -> np.ndarray:
        """manhattan distance"""
        return np.sum(np.abs(locations - fromPos), axis=1)

    @staticmethod
    def closest(locations: np.ndarray, fromPos:np.ndarray) -> np.ndarray:
        distances = Utils.distanceToLocations(locations, fromPos)
        return locations[np.argmin(distances)]
    
    @staticmethod
    def distance(a: np.ndarray, b: np.ndarray) -> float:
        """manhattan distance"""
        return np.sum(np.abs(a - b))

        
    