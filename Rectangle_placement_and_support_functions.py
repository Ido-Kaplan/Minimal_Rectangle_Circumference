# file contains the rectangle placement algorithms, and support functions, such as random rectangle list generation,
# random permutation generation for rectangle list and rectangle structure presentation

from random import randint
import numpy as np
import tkinter
from Geometric_shapes import Point, Rectangle, Placed_Rectangles_List
from Parameters import *

def get_rec_permutation(rec_list):
    permutated_rec_list = []
    chosen_permutation = np.random.permutation(len(rec_list))
    for index in chosen_permutation:
        permutated_rec_list.append(rec_list[index])
    return permutated_rec_list

def generate_random_rectangle_list(N=10, max_side_length=100):
    rectangle_list = []
    for i in range(N):
        a = randint(0, max_side_length)
        b = randint(0, max_side_length)
        c = randint(0, max_side_length)
        d = randint(0, max_side_length)

        # in order to ensure no side of a rectangle is zero
        while a == b or a == c or a == d or b == c or b == d or c == d:
            a = randint(0, max_side_length)
            b = randint(0, max_side_length)
            c = randint(0, max_side_length)
            d = randint(0, max_side_length)

        x_min, x_max, y_min, y_max = sorted([a, b, c, d])
        upper_right_corner = Point(x_max, y_max)
        upper_left_corner = Point(x_min, y_max)
        lower_right_corner = Point(x_max, y_min)
        lower_left_corner = Point(x_min, y_min)
        rectangle_list.append(Rectangle(upper_right_corner, upper_left_corner, lower_right_corner, lower_left_corner))
    return rectangle_list


def draw_rectangles_structure(placed_rectangles):
    presentation_factor = 5   # multiplies the rectangles width and height, makes them more presentable
    min_dist_from_sides = 10  # small buffering between edges of screen

    total_width = placed_rectangles.max_x - placed_rectangles.min_x
    total_height = placed_rectangles.max_y - placed_rectangles.min_y

    screen_width = int(total_width * (presentation_factor)) + min_dist_from_sides
    screen_height = int(total_height * (presentation_factor)) + min_dist_from_sides

    root = tkinter.Tk()

    geometry = str(screen_width + 2 * min_dist_from_sides) + "x" + str(screen_height + 2 * min_dist_from_sides)
    root.geometry(geometry)
    root.title('Rectangle structure placement')
    canvas = tkinter.Canvas(root, width=screen_width,
                            height=screen_height, bg='white')

    for rec in placed_rectangles.rec_list:
        x0 = (rec.get_min_x() - placed_rectangles.min_x) * presentation_factor + min_dist_from_sides
        y0 = (rec.get_min_y() - placed_rectangles.min_y) * presentation_factor + min_dist_from_sides
        x1 = (rec.get_max_x() - placed_rectangles.min_x) * presentation_factor + min_dist_from_sides
        y1 = (rec.get_max_y() - placed_rectangles.min_y) * presentation_factor + min_dist_from_sides
        canvas.create_rectangle((x0, y0), (x1, y1), fill="gray")

    canvas.pack(anchor=tkinter.CENTER, expand=True)

    root.mainloop()


def greedy_algo(rec_list):
    placed_rectangles = Placed_Rectangles_List([rec_list[0]])  # initialize the list with the first given rectangle
    for i in range(1, len(rec_list)):
        rec_to_add = rec_list[i]

        # initialize the best_circumference value to have the biggest circumference possible
        best_circumference = placed_rectangles.return_block_rec_circumference() + rec_to_add.get_circumference()
        best_location = Point(placed_rectangles.max_x, placed_rectangles.max_y)
        if enable_hole_reduction:
            best_structure_hole_indicators = placed_rectangles.get_hole_indicators_list()

        # check the corners of each placed rectangle
        for placed_rec in placed_rectangles.rec_list:
            for location in placed_rec.get_possible_neighbor_locations(rec_to_add):

                # update the location of the rectangle we want to add to the list according to the current corner
                rec_to_add.update_location(location)
                if placed_rectangles.legal_to_add_rec(rec_to_add):

                    # if the circumference is smaller, choose this placement
                    if best_circumference > placed_rectangles.check_circumference_for_add_rec(rec_to_add):
                        best_circumference = placed_rectangles.check_circumference_for_add_rec(rec_to_add)
                        best_location = location

                    # if the circumference is the same, and hole reduction is enabled, place rectangle in the location
                    # which reduces the number of holes OR place rectangle in existing hole
                    elif best_circumference == placed_rectangles.check_circumference_for_add_rec(
                            rec_to_add) and enable_hole_reduction:

                        current_structure_hole_indicators = placed_rectangles.get_hole_indicators_list(rec_to_add)

                        placed_rec_inside_hole = False
                        for best_hole_indicator in best_structure_hole_indicators:
                            if rec_to_add.point_in_rectangle(best_hole_indicator):
                                placed_rec_inside_hole = True
                                break

                        if len(current_structure_hole_indicators) < len(
                                best_structure_hole_indicators) or placed_rec_inside_hole:
                            best_location = location

        rec_to_add.update_location(best_location)
        placed_rectangles.add_rec_to_list(rec_to_add)

    return placed_rectangles


def get_at_most_mean_greedy_result(rec_list, initial_circumference):
    # choose permutation which reduces the greedy algorithm the most
    best_permutation = rec_list
    best_circumference = initial_circumference

    # by running log2(1/delta) times, we ensure that we get at most the mean greedy algorithm result, with success rate
    # of 1-delta (if delta=0.001, then we have 99.9% success rate)
    for i in range(1 + int(np.log2(1 / delta))):
        permutated_rec_list = get_rec_permutation(rec_list)
        cur_placed_rectangles = greedy_algo(permutated_rec_list)
        if best_circumference > cur_placed_rectangles.return_block_rec_circumference():
            best_circumference = cur_placed_rectangles.return_block_rec_circumference()
            best_permutation = permutated_rec_list

    return greedy_algo(best_permutation)
