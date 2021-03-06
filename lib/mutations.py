import numpy.random as rand
from copy import deepcopy

# Switch two random points in a path
def mutatePath(path, mutations):
    for _ in range(rand.randint(1, mutations + 1)):
        length = len(path.values)
        # Make sure p1 != p2
        p1 = rand.randint(0, length - 1)
        p2 = p1
        while p1 == p2:
            p2 = rand.randint(0, length - 1)
        # Switch points
        path.values[p1], path.values[p2] = path.values[p2], path.values[p1]
    return deepcopy(path)

# Switch subsections of a path
def shufflePath(path, size):
    # Subset start
    start = rand.randint(0, len(path.values) - 1)
    # Subset length
    subsetLength = rand.randint(2, size)
    # Define subset
    subset = deepcopy(path.values[start:start + subsetLength])
    # Remove subset from path
    path.values = deepcopy(path.values[:start]) + deepcopy(path.values[start + subsetLength:])
    # Choose where the subset is inserted
    insert = rand.randint(0, len(path.values) - 1)
    # Insert subset
    path.values = deepcopy(path.values[:insert]) + deepcopy(subset) + deepcopy(path.values[insert:])
    return deepcopy(path)

''' Not sure about this '''
def tidy(path, fitnessFunction, lookupTable):
    # For every point of a path
    for i in range(1, len(path.values)):
        # Store the current distance
        oldDistance = path.fitness
        # Switch over two consecutive points
        path.values[i-1], path.values[i] = path.values[i], path.values[i-1]
        # Evaluate the new distance
        path.evaluate(fitnessFunction, lookupTable)
        # If the old distance is better revert the change
        if path.fitness > oldDistance:
            path.values[i-1], path.values[i] = path.values[i], path.values[i-1]
