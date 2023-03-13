import numpy as np
from adl.stats.map_stats import ClusterType

class VisualUtils:
    
    @staticmethod
    def addClustersToImg(img: np.ndarray, clusters: ClusterType, color=255):
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