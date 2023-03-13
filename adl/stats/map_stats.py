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
class MapStats:
    nIceTiles: int
    nOreTiles: int
    nHighRubble: int
    nLowRubble: int
    iceClusters: ClusterType
    oreClusters: ClusterType
    resourceClusters: ClusterType
        

    



    
        





