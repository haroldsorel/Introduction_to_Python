import random

my_list = [2, 1, 3, 0, - 3, 666, -69, 2000, -1000]


def check_if_sorted():
    res = True
    if my_list == sorted(my_list):
        res = False
    return res


def random_number_generator():
    return random.randint(0, len(my_list) - 1)


while check_if_sorted():
    x = random_number_generator()
    y = random_number_generator()
    my_list[x], my_list[y] = my_list[y], my_list[x]
    print(my_list)
