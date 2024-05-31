import random
import math

# contraints
weights = [21, 12, 30, 24, 45, 47, 41, 36, 38, 45, 4, 17, 1, 42, 26, 19, 12, 27, 15, 4, 5, 4, 21, 7, 23, 45, 18, 7, 29, 44, 18, 3, 8, 4, 38, 23, 34, 35, 29, 32, 44, 34, 44, 24, 8, 4, 36, 16, 34, 33, 27, 36, 26, 25, 25, 47, 20, 6, 13, 35, 42, 49, 11, 39, 30, 21, 26, 25, 33, 38, 16, 5, 42, 20, 39, 9, 6, 46, 44, 50, 44, 2, 28, 50, 26, 44, 4, 50, 47, 29, 22, 17, 37, 1, 19, 47, 28, 24, 25, 16]
values = [96, 99, 52, 100, 46, 43, 22, 20, 84, 73, 53, 83, 52, 56, 22, 59, 15, 6, 69, 61, 22, 41, 63, 56, 13, 17, 1, 42, 49, 16, 67, 2, 12, 96, 98, 4, 50, 87, 25, 84, 82, 63, 1, 38, 91, 69, 38, 64, 25, 58, 99, 85, 29, 69, 36, 99, 9, 26, 82, 9, 54, 81, 74, 15, 44, 36, 48, 59, 15, 91, 65, 17, 57, 94, 79, 69, 47, 27, 57, 25, 32, 92, 89, 80, 93, 18, 52, 63, 92, 67, 39, 75, 82, 61, 9, 93, 6, 53, 12, 39]
limit = 1500
items = len(weights)

# constants
temperature = 8000
iterations = 120
step_size = 50
final_temperature = 5


def objective_function(knapsack):
    """
    objective function value calculated as the sum of values picked by the
    knapsack configuration

    """
    objective_value = 0
    weight_sum = 0    
    for i in range(len(knapsack)):
        objective_value = objective_value + knapsack[i]*values[i]
        weight_sum = weight_sum + knapsack[i]*weights[i]
    
    if weight_sum > limit:
        objective_value = 0
    
    return objective_value

def flipped(bit):
    """
    returns the complement of the supplied bit

    """
    if bit == 0:
        return 1
    else:
        return 0


def find_neighbours(member):
    """
    finds all neighbours with a 1 bit difference to the supplied 
    configuration

    """

    neighbours = []
    for i in range(len(member)):
        single_neighbour = member[0:i] + [flipped(member[i])] + member[(i+1):]
        neighbours.append(single_neighbour)
    
    return neighbours

def generate_initial_permutation():
    """
    generates an initial configuration

    """
    member = [
        random.choice([0,1])
        for i in range(items)
    ]

    return member

def simulated_annealing():
    """
    The neighbour with the better objective function value is
    selected at every step.

    The metropolis acceptance criterion is used
    in order to prevent rapid convergence to local optima.

    """
    initial_objective = 0

    while initial_objective == 0:
        initial_config = generate_initial_permutation()
        initial_objective = objective_function(initial_config)

    best_config = initial_config
    best_objective = initial_objective
    coefficient = 1

    metrics = {}
    metrics["solutions_checked"] = 0
    metrics["improvements"] = 0
    metrics["random_steps"] = 0

    while temperature/coefficient > final_temperature:

        i = 0
        improvements_current = 0
        random_steps_current = 0

        while i < step_size:

            metrics["solutions_checked"] += 1
            list_of_neighbours = find_neighbours(initial_config)
            random_neighbour = list_of_neighbours[random.randint(0, len(list_of_neighbours)-1)]
            random_neighbour_objective = objective_function(random_neighbour)
            if random_neighbour_objective > best_objective:
                best_objective = random_neighbour_objective
                best_config = random_neighbour
                improvements_current += 1
            else:
                delta = best_objective - random_neighbour_objective
                random_value = random.uniform(0,1)
                metropolis_criterion = math.exp(-1*delta*coefficient / temperature)
                if(metropolis_criterion > random_value):
                    best_objective = random_neighbour_objective
                    best_config = random_neighbour
                    random_steps_current += 1
            i += 1
        
        metrics["improvements"] += improvements_current
        metrics["random_steps"] += random_steps_current
        coefficient += 1

    metrics["best_config"] = best_config
    metrics["best_objective"] = best_objective

    return metrics



def main():
    metrics = simulated_annealing()
    print(metrics["best_objective"])


