# Minimal Rectangle Circumference

In this repository, we test algorithms which minimize the circumference of a rectangle which contains a structure made from an array of input rectangles.

An example was given in the main module: for a randomly generated rectangle list, the code prints out the total circumference of all rectangles in the
rectangle list, the circumference structure calculated using a greedy algorithm, and presents the rectangle structure to the user.

The running time of the algorithm is O(n^3), where n is the number of rectangles in the list, or O(n^4) is hole reduction mode is enabled; more precisely, the running time
is multiplied by log2(1/delta), since we run the greedy algorithm log2(1/delta) times and return the minimal output of these runs.

# Parameters

There are couple of parameters in Parameters.py file; the most significant ones are:

* N                      - number of rectangles in the rectangle list.

* delta                  - chance to get above mean result when taking random permutations for the greedy algorithm.

* enable_hole_reduction  - if this mode is enabled, we require the algorithm, as a second condition, to minimize
                                the number of holes inside the rectangles structure, and to favor placing rectangles
                                 inside existing holes.

(*) In this context, a hole is defined by a space within the rectangle structure surrounded by four walls, by not necessarily closed off entirely;
  Even if there's a path between the space within the rectangle structure to the outer side of the structure, it can still be regarded as a hole.