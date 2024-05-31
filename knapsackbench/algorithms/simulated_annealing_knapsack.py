import random
import math

# contraints
weights = []
values = []
limit = 0
items = 0

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
    metrics["improvements"] = 0
    metrics["random_steps"] = 0
    metrics["solutions_history"] = []

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
        metrics["solutions_history"].append(best_objective)
        coefficient += 1

    metrics["best_config"] = best_config
    metrics["best_objective"] = best_objective

    return metrics



def main(request):
    global weights, values, limit, items

    weights = request.weights
    values = request.values
    limit = request.limit
    items = request.items

    metrics = simulated_annealing()
    return metrics


