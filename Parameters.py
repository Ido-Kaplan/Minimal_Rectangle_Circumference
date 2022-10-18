max_side_length = 100         # maximal length of a side of a rectangle (needed for random the rectangle list generation)

N = 20                        # number of rectangles in the rectangle list

delta = 0.001                 # chance to get above mean result when taking random permutations for the greedy algorithm

Resolution = 1.0              # the minimal distance between two rectangles. It is set to 1.0 since the rectangle
                              # placement is set with integers.

enable_hole_reduction = False # if this mode is enabled, we require the algorithm, as a second condition, to minimize
                              # the number of holes inside the rectangles structure, and to favor placing rectangles
                              # inside existing holes.
