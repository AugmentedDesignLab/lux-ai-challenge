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
    def addClustersToImg(img: np.ndarray, clusters, color=255):
        scaleFactor = int((img.shape[0] / 48))
        padding = int(scaleFactor / 2)
        for center in clusters:

            centerX = int(center[0] * scaleFactor)
            centerY = int(center[1] * scaleFactor)
            # print(center, centerX, centerY)

            xSlice = slice(max(0, centerX - padding), min(640, centerX + padding))
            ySlice = slice(max(0, centerY - padding), min(640, centerY + padding))

            # print(xSlice, ySlice)
            img[ySlice, xSlice] = color
    