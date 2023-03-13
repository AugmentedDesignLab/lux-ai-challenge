from .map_stats import MapStats, ClusterType
from lux.kit import GameState, obs_to_game_state, Board

class ClusterAnalyzer:
    def getClusterQuality(self, mapStats: MapStats, game_state: GameState):
        totalRubbleInside = 0
        totalRubbleOutside = 0

        # rubble indicates how fast we can get to a resource or how much lichen we can grow. Eventually, we must clean the rubbles.

        # a resource cluster is great if it's near an ice cluster and a ore cluster??? NO!
    
    def rubbleToClosestIce(self, mapStats: MapStats, game_state: GameState):
        pass
        


