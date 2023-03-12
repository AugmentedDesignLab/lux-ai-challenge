from collections import defaultdict, Counter
from dataclasses import dataclass
from luxai_s2.env import LuxAI_S2
import logging
import math
import numpy as np
from typing import *

from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

from adl.board_analysis import BoardAnalyzer
from lux.kit import GameState, Board, obs_to_game_state

ClusterType = Dict[np.ndarray, Dict[str, int]]

@dataclass
class MapStat:
    nIceTiles: int
    nOreTiles: int
    nHighRubble: int
    nLowRubble: int
    iceClusters: ClusterType
    oreClusters: ClusterType
    resourceClusters: ClusterType
        


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
        interClusterDistance = idealDiameter // 2
        return MapStat(
            nIceTiles = np.sum(game_state.board.ice),
            nOreTiles = np.sum(game_state.board.ore),
            nHighRubble = np.sum(game_state.board.rubble > 50),
            nLowRubble = np.sum(game_state.board.rubble <= 50),
            iceClusters = self.getResourceCluster(game_state, "ice"),
            oreClusters = self.getResourceCluster(game_state, "ore"),
            resourceClusters = self.getResourceCluster(game_state)
        )
    
    def getResourceCluster(self, game_state: GameState, rType=None) -> ClusterType:
        """
        we return clusters where distortion <= interClusterDistance
        """
        board = game_state.board
        maxFactories = game_state.maxFactoriesPerPlayer * 2
        idealDiameter = self.boardAnalyzer.idealDiameter(game_state)
        interClusterDistance = idealDiameter // 2

        distortions = []
        distMapping = {}
        models = {}

        if rType is None:
            resourceMap = np.logical_or(board.ice, board.ore)
        elif rType == "ice":
            resourceMap = board.ice == 1
        elif rType == "ore":
            resourceMap = board.ore == 1

        X = np.argwhere(resourceMap == True)

        maxK = min(int(np.sum(resourceMap)), maxFactories)
        K = range(1, maxK+1)

        for k in K:
            # Building and fitting the model

            # for each k, we try 5 different initializations
            kmeanModel = None
            minDistortion = math.inf
            for randomState in range(5):
                candidateModel = KMeans(n_clusters=k, n_init="auto", random_state=randomState).fit(X)
                candidateModel.fit(X)
                distortion = sum(np.min(cdist(X, candidateModel.cluster_centers_,
                                                'euclidean'), axis=1)) / X.shape[0]
                if distortion < minDistortion:
                    minDistortion = distortion
                    kmeanModel = candidateModel


            models[k] = kmeanModel
        
            distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                                'euclidean'), axis=1)) / X.shape[0])
        
            distMapping[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X.shape[0]

        bestK = None
        for key, val in distMapping.items():
            self.logger.info(f'{key} : {val}')

            bestK = key
            if val < interClusterDistance:
                break

        self.logger.info(f'best K : {bestK}')

        # now we need the centers, and cluster sizes
        bestModel = models[bestK]
        centers = [tuple(c) for c in bestModel.cluster_centers_.astype(int)]

        # now size of each cluster

        clusters = defaultdict(lambda: defaultdict())
        iceMembership = bestModel.predict(game_state.iceLocations)
        oreMembership = bestModel.predict(game_state.oreLocations)

        centerIdxFreq = Counter(iceMembership)
        for centerIdx, n in centerIdxFreq.items():
            clusters[centers[centerIdx]] = {"ice": n}

        centerIdxFreq = Counter(oreMembership)
        for centerIdx, n in centerIdxFreq.items():
            clusters[centers[centerIdx]]["ore"] = n




        # return
        # cluster centers, # of resources in each cluster.
        return clusters

    



    
        





