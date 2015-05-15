import numpy as np
from copy import deepcopy

# Support any number of dimensions
def euclidian(p1, p2):
    return np.sqrt(np.sum(((p1[i] - p2[i]) ** 2 for i in range(len(p1)))))

''' To verify '''
def haversine(p1, p2):
    lat1, lat2, lon1, lon2 = map(np.radians, deepcopy([p1[0], p1[1], p2[0], p2[1]]))
    lon = lon2 - lon1
    lat = lat2 - lat1
    a = np.sin(lat/2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon/2) ** 2
    return np.arcsin(np.sqrt(a)) * 12742 # Diameter of the Earth in kilometers

''' To do: google distance API '''
