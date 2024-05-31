import random
import math
import copy


# contraints
weights = [21, 12, 30, 24, 45, 47, 41, 36, 38, 45, 4, 17, 1, 42, 26, 19, 12, 27, 15, 4, 5, 4, 21, 7, 23, 45, 18, 7, 29, 44, 18, 3, 8, 4, 38, 23, 34, 35, 29, 32, 44, 34, 44, 24, 8, 4, 36, 16, 34, 33, 27, 36, 26, 25, 25, 47, 20, 6, 13, 35, 42, 49, 11, 39, 30, 21, 26, 25, 33, 38, 16, 5, 42, 20, 39, 9, 6, 46, 44, 50, 44, 2, 28, 50, 26, 44, 4, 50, 47, 29, 22, 17, 37, 1, 19, 47, 28, 24, 25, 16]
values = [96, 99, 52, 100, 46, 43, 22, 20, 84, 73, 53, 83, 52, 56, 22, 59, 15, 6, 69, 61, 22, 41, 63, 56, 13, 17, 1, 42, 49, 16, 67, 2, 12, 96, 98, 4, 50, 87, 25, 84, 82, 63, 1, 38, 91, 69, 38, 64, 25, 58, 99, 85, 29, 69, 36, 99, 9, 26, 82, 9, 54, 81, 74, 15, 44, 36, 48, 59, 15, 91, 65, 17, 57, 94, 79, 69, 47, 27, 57, 25, 32, 92, 89, 80, 93, 18, 52, 63, 92, 67, 39, 75, 82, 61, 9, 93, 6, 53, 12, 39]
limit = 1500
items = len(weights)

# constants
alpha = 3
beta = 2
ant_count = 10
rho = 0.2
iterations = 500

# dictionary of {index : [value, weight]} elements
complete_search_space = {i : [int(values[i]), int(weights[i])] for i in range(items)}

# tau defaults to 10 before ACO
tau = {i : 10 for i in range(items)}

# formula used for attractiveness (mu) = value/(weight/knapsack capacity)
mu =  {i : (values[i]*limit/weights[i]) for i in range(items)}

def generate_transition_list(search_space):
    """
    Calculates the probability to be selected for each element in the knapsack.
    
    """
    tau_mu_summation = 0
    for i in search_space.keys():
        tau_mu_summation += ((tau[i]**alpha)*(mu[i]**beta))
    
    probability_list = {
        i : ((tau[i]**alpha)*(mu[i]**beta))/tau_mu_summation for i in search_space.keys()
    }

    return probability_list

def update_search_space(current_search_space, current_capacity, item_picked):
    """
    Updates the search space after a selection by an ant.
    The elements whose weight exceeds the current capacity and the chosen item are removed from the search space. 
    
    """

    updated_search_space = copy.deepcopy(current_search_space)
    items_to_be_removed = []

    for i in current_search_space.keys():
        if current_capacity < updated_search_space[i][1]:
            items_to_be_removed.append(i)
    
    if item_picked not in items_to_be_removed:
        items_to_be_removed.append(item_picked)

    for i in items_to_be_removed:
        del updated_search_space[i]
    
    return updated_search_space


def sample_item(probability_list):
    """
    returns an index for a random item according to roulette selection
    """
    random_value = random.random()
    total = 0

    for key, value in probability_list.items():
        total += value

        if random_value <= total:
            return key
        
    
    assert False, 'unreachable'


def normalise(probability_list):
    """
    Normalises the probabilities generated to sum up to 1.
    """
    sum_of_probabilities = 0
    for i in probability_list:
        sum_of_probabilities += probability_list[i]
    for i in probability_list:
        probability_list[i] = probability_list[i]/sum_of_probabilities
    return probability_list

def update_pheromones(result_of_k_ants, global_profit):
    """
    updates global pheromone values for each element in the knapsack
    """
    for i in result_of_k_ants:
        z = result_of_k_ants[i][0]
        delta_tau = (1/(1+ ((global_profit-z)/global_profit)))
        for j in result_of_k_ants[i][1].keys():
            tau[j] = tau[j] + delta_tau
    return tau

def evaporate():
    """
    controls evaporation rate for pheromones
    """
    for i in tau.keys():
        tau[i] = max(0.05, tau[i]*rho)
    return tau


def ant_colony_optimisation(probability_list):

    iteration_number = 0
    global_profit = -1
    global_profit_tracker = []
    global_solution_set = {}

    while iteration_number < iterations:

        current_search_space = complete_search_space
        current_capacity = limit
        result_of_k_ants = {}
        ant_profit = -1
        ant_solution_set = {}

        for ant in range(ant_count):

            local_profit = 0
            local_solution_set = {}

            while current_capacity > 0 and len(current_search_space.keys()) > 0:
                
                
                current_keys = current_search_space.keys()
                current_probability_list = normalise(dict((j, probability_list[j]) for j in current_keys if j in probability_list))

                item = sample_item(current_probability_list)
                local_solution_set[item] = current_search_space[item]
                current_capacity -= current_search_space[item][1]
                local_profit += current_search_space[item][0]
                current_search_space = update_search_space(current_search_space, current_capacity, item)

            if local_profit > ant_profit:
                ant_profit = local_profit
                ant_solution_set = local_solution_set
            
            result_of_k_ants[ant] = [local_profit, local_solution_set]

        
        if ant_profit > global_profit:
            global_profit = ant_profit
            global_solution_set = ant_solution_set
            global_profit_tracker.append(global_profit)

        tau = update_pheromones(result_of_k_ants, global_profit)
        tau = evaporate()

        probability_list = generate_transition_list(complete_search_space)
        iteration_number += 1
    

    ant_colony_data = {}
    ant_colony_data["total_profit"] = global_profit
    ant_colony_data["profit_history"] = global_profit_tracker
    ant_colony_data["solution_set"] = global_solution_set

    return ant_colony_data
        

def main():

    ant_colony_data = generate_transition_list(complete_search_space)
    return ant_colony_data





