from collections import defaultdict, Counter
from dataclasses import dataclass
from luxai_s2.env import LuxAI_S2
import logging
import math
import numpy as np
from typing import *
import os
import dill
os.environ["OMP_NUM_THREADS"] = '1'

from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

from adl.board_analysis import BoardAnalyzer
from adl.utils import Utils
from lux.kit import GameState, Board, obs_to_game_state
from .map_stats import MapStats, ClusterType

class MapStatsManager:
    def __init__(self):
        self.logger = logging.getLogger("MapStatsManager")
        self.boardAnalyzer = BoardAnalyzer()
        self.seedStats = defaultdict() # seed -> stats

    def generate(self, seedStart = 0, seedEnd = 100):
        env = LuxAI_S2()
        for seed in range(seedStart, seedEnd):
            obs = env.reset(seed=seed) # resets an environment with a seed
            game_state = obs_to_game_state(0, env.state.env_cfg, obs["player_0"])
            self.seedStats[seed] = self.collectMapStats(game_state)
        
        self.flushStats(seedStart, seedEnd)
        return True
    
    def flushStats(self, seedStart, seedEnd):
        if not os.path.exists("./logs"):
            os.mkdir("./logs")

        with open(f"./logs/{seedStart}-{seedEnd-1}", "wb") as f:
            dill.dump(self.seedStats, f)

        

    
    def collectMapStats(self, game_state: GameState) -> MapStats:
        idealDiameter = self.boardAnalyzer.idealDiameter(game_state)
        interClusterDistance = idealDiameter // 2
        return MapStats(
            nIceTiles = np.sum(game_state.board.ice),
            nOreTiles = np.sum(game_state.board.ore),
            nTotalRubble = np.sum(game_state.board.rubble),
            nHighRubble = np.sum(game_state.board.rubble > 50),
            nLowRubble = np.sum(game_state.board.rubble <= 50),
            iceClusters = self.getResourceCluster(game_state, "ice"),
            oreClusters = self.getResourceCluster(game_state, "ore"),
            resourceClusters = self.getResourceCluster(game_state),
            factoriesPerPlayer = game_state.maxFactoriesPerPlayer,
            resourcePerPlayer = game_state.env_cfg.INIT_WATER_METAL_PER_FACTORY,
            costLichen = game_state.env_cfg.LICHEN_WATERING_COST_FACTOR,
            costLight = game_state.env_cfg.ROBOTS["LIGHT"].METAL_COST,
            costHeavy = game_state.env_cfg.ROBOTS["HEAVY"].METAL_COST,
            costFactory = game_state.env_cfg.FACTORY_WATER_CONSUMPTION,
            chargeFactory = game_state.env_cfg.FACTORY_CHARGE,
            chargeLight = game_state.env_cfg.ROBOTS["LIGHT"].CHARGE,
            chargeHeavy = game_state.env_cfg.ROBOTS["HEAVY"].CHARGE,
        )
    
    def getInterClusterDistance(self, game_state: GameState) -> int:
        
        idealDiameter = self.boardAnalyzer.idealDiameter(game_state)
        return idealDiameter // 2

    def getResourceCluster(self, game_state: GameState, rType=None) -> ClusterType:
        """
        we return clusters where distortion <= interClusterDistance
        """
        board = game_state.board
        maxFactories = game_state.maxFactoriesPerPlayer * 2
        interClusterDistance = self.getInterClusterDistance(game_state)

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
            self.logger.debug(f'{key} : {val}')

            bestK = key
            if val < interClusterDistance:
                break

        self.logger.debug(f'best K : {bestK}')

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
            clusters[centers[centerIdx]]["closest_ice"] = Utils.closest(game_state.iceLocations, centers[centerIdx])


        centerIdxFreq = Counter(oreMembership)
        for centerIdx, n in centerIdxFreq.items():
            clusters[centers[centerIdx]]["ore"] = n
            clusters[centers[centerIdx]]["closest_ore"] = Utils.closest(game_state.oreLocations, centers[centerIdx])


        self.addRubbles(game_state, clusters, interClusterDistance)


        # return
        # cluster centers, # of resources in each cluster.
        return clusters


    def addRubbles(self, game_state: GameState, clusters: ClusterType, interClusterDistance: int):
        boardSize = game_state.board.ice.shape[0]
        for center, info in clusters.items():
            xSlice = slice(max(0, center[0] - interClusterDistance), min(boardSize, center[0] + interClusterDistance))
            ySlice = slice(max(0, center[1] - interClusterDistance), min(boardSize, center[1] + interClusterDistance))
            rubbles = game_state.board.rubble[xSlice, ySlice]
            info["rubble"] = np.sum(rubbles)
            # clusters[center] = info
            # print(info)


    



    
        





