from Rectangle_placement_and_support_functions import *

if __name__=="__main__":

    # generate a random list of rectangles, sort them by their circumference - only as the initial permutation,
    # other permutations will be tested afterwards
    rectangle_list = generate_random_rectangle_list(N,max_side_length)
    rectangle_list = sorted(rectangle_list, key = lambda x: x.get_circumference(), reverse=True)

    # print maximal possible circumference
    maximal_rec_circumference = 0
    for rec in rectangle_list:
        maximal_rec_circumference += rec.get_circumference()
    print("The total circumference of all rectangles:",maximal_rec_circumference)

    # run a single greedy iteration with the initial permutation
    initial_circumference = greedy_algo(rectangle_list).return_block_rec_circumference()

    # get at most mean greedy result, for different rectangle list permutations
    best_permutated_choice = get_at_most_mean_greedy_result(rectangle_list,initial_circumference)
    print(best_permutated_choice)
    draw_rectangles_structure(best_permutated_choice)