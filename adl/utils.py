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