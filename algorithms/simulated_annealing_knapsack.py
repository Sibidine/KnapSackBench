import random

# contraints
weights = [21, 12, 30, 24, 45, 47, 41, 36, 38, 45, 4, 17, 1, 42, 26, 19, 12, 27, 15, 4, 5, 4, 21, 7, 23, 45, 18, 7, 29, 44, 18, 3, 8, 4, 38, 23, 34, 35, 29, 32, 44, 34, 44, 24, 8, 4, 36, 16, 34, 33, 27, 36, 26, 25, 25, 47, 20, 6, 13, 35, 42, 49, 11, 39, 30, 21, 26, 25, 33, 38, 16, 5, 42, 20, 39, 9, 6, 46, 44, 50, 44, 2, 28, 50, 26, 44, 4, 50, 47, 29, 22, 17, 37, 1, 19, 47, 28, 24, 25, 16]
values = [96, 99, 52, 100, 46, 43, 22, 20, 84, 73, 53, 83, 52, 56, 22, 59, 15, 6, 69, 61, 22, 41, 63, 56, 13, 17, 1, 42, 49, 16, 67, 2, 12, 96, 98, 4, 50, 87, 25, 84, 82, 63, 1, 38, 91, 69, 38, 64, 25, 58, 99, 85, 29, 69, 36, 99, 9, 26, 82, 9, 54, 81, 74, 15, 44, 36, 48, 59, 15, 91, 65, 17, 57, 94, 79, 69, 47, 27, 57, 25, 32, 92, 89, 80, 93, 18, 52, 63, 92, 67, 39, 75, 82, 61, 9, 93, 6, 53, 12, 39]
limit = 1500
items = len(weights)

# constants
area = [0,items**2-1]
temperature = 12
iterations = 1200
step_size = 0.1


def objective_function(knapsack):

    objective_value = 0
    weight_sum = 0    
    for i in range(len(knapsack)):
        objective_value = objective_value + knapsack[i]*values[i]
        weight_sum = weight_sum + knapsack[i]*weights[i]
    
    if weight_sum > limit:
        objective_value = 0
    
    return objective_value


def convert_number_to_binary(number):

    binary_number = []
    while number > 0:
        binary_number.append(number % 2)
        number = number//2
    
    return list(reversed(binary_number))


