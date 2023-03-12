from collections import defaultdict, Counter
from dataclasses import dataclass
from luxai_s2.env import LuxAI_S2
import logging
import numpy as np
from typing import *

from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

from adl.board_analysis import BoardAnalyzer
from lux.kit import GameState, obs_to_game_state

@dataclass
class MapStat:
    nIceTiles: int
    nOreTiles: int
    nHighRubble: int
    nLowRubble: int
    nIceCluser: int
    nOreCluser: int
        


class MapStatsManager:
    def __init__(self):
        self.logger = logging.getLogger("MapStatsManager")
        self.boardAnalyzer = BoardAnalyzer()
        self.seedStats = defaultdict() # seed -> stats

    def generate(self, seedStart = 0, seedEnd =100):
        env = LuxAI_S2()
        for seed in range(seedStart, seedEnd):
            obs = env.reset(seed=seed) # resets an environment with a seed
            game_state = obs_to_game_state(0, env.state.env_cfg, obs["player_0"])
            self.seedStats[seed] = self.collectMapStats(game_state)
    
    def collectMapStats(self, game_state: GameState) -> MapStat:
        idealDiameter = self.boardAnalyzer.idealDiameter(game_state)
        interCluserDistance = idealDiameter // 2
        return MapStat(
            nIceTiles = np.sum(game_state.board.ice),
            nOreTiles = np.sum(game_state.board.ore),
            nHighRubble = np.sum(game_state.board.rubble > 50),
            nLowRubble = np.sum(game_state.board.rubble <= 50),
            nIceCluser = self.getResourceCluster(game_state.board.ice, interCluserDistance, game_state.maxFactoriesPerPlayer * 2),
            nOreCluser = self.getResourceCluster(game_state.board.ore == 1, interCluserDistance, game_state.maxFactoriesPerPlayer * 2)
        )
    
    def getResourceCluster(self, resourceMap: np.ndarray, interCluserDistance: int, maxFactories: int) -> Dict[np.ndarray, int]:
        """
        we return clusters where distortion <= interCluserDistance
        """

        clusterMembership = defaultdict()
        currentClusters = [] # list of lists

        distortions = []
        distMapping = {}
        models = {}

        X = np.argwhere(resourceMap == 1)

        maxK = min(int(np.sum(resourceMap)), maxFactories)
        K = range(1, maxK+1)

        for k in K:
            # Building and fitting the model
            kmeanModel = KMeans(n_clusters=k, n_init="auto").fit(X)
            kmeanModel.fit(X)
            models[k] = kmeanModel
        
            distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                                'euclidean'), axis=1)) / X.shape[0])
        
            distMapping[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X.shape[0]

        bestK = None
        for key, val in distMapping.items():
            self.logger.info(f'{key} : {val}')

            bestK = key
            if val < interCluserDistance:
                break

        self.logger.info(f'best K : {bestK}')

        # now we need the centers, and cluster sizes
        bestModel = models[bestK]
        centers = bestModel.cluster_centers_

        # now size of each cluster
        clutersSizes = defaultdict()
        membership = bestModel.predict(X)
        centerIdxFreq = Counter(membership)
        print("centerIdxFreq", centerIdxFreq)

        for centerIdx, n in centerIdxFreq.items():
            clutersSizes[centers[centerIdx]] = n




        # return
        # cluster centers, # of resources in each cluster.
        return clutersSizes


    
        





