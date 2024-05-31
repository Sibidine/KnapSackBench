import random
import math
import copy

# constants
alpha = 3
beta = 2
ant_count = 10
rho = 0.2
iterations = 500

   

def generate_transition_list(search_space, tau, mu):
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

def update_pheromones(result_of_k_ants, global_profit, tau):
    """
    updates global pheromone values for each element in the knapsack
    """
    for i in result_of_k_ants:
        z = result_of_k_ants[i][0]
        delta_tau = (1/(1+ ((global_profit-z)/global_profit)))
        for j in result_of_k_ants[i][1].keys():
            tau[j] = tau[j] + delta_tau
    return tau

def evaporate(tau):
    """
    controls evaporation rate for pheromones
    """
    for i in tau.keys():
        tau[i] = max(0.05, tau[i]*rho)
    return tau


def ant_colony_optimisation(probability_list, weights, values, items, limit, complete_search_space, tau, mu):

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

        tau = update_pheromones(result_of_k_ants, global_profit, tau)
        tau = evaporate(tau)

        probability_list = generate_transition_list(complete_search_space, tau, mu)
        iteration_number += 1
    

    ant_colony_data = {}
    ant_colony_data["max_profit"] = global_profit
    ant_colony_data["profit_history"] = global_profit_tracker
    
    solution_set = []
    for i in range(100):
        if i in global_solution_set.keys():
            solution_set.append(1)
        else:
            solution_set.append(0)
    ant_colony_data["solution_set"] = solution_set


    return ant_colony_data
        

def main(request):

    weights = request.weights
    values = request.values
    items = request.items
    limit = request.limit


    # dictionary of {index : [value, weight]} elements
    complete_search_space = {i : [int(values[i]), int(weights[i])] for i in range(items)}

    # tau defaults to 10 before ACO
    tau = {i : 10 for i in range(items)}

    # formula used for attractiveness (mu) = value/(weight/knapsack capacity)
    mu =  {i : (values[i]*limit/weights[i]) for i in range(items)}

    probability_list = generate_transition_list(complete_search_space, tau, mu)
    return ant_colony_optimisation(probability_list, weights, values, items, limit, complete_search_space, tau, mu)





