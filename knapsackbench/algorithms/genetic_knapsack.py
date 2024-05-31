import random

# contraints
weights = []
vallues = []
limit = 0
items = 0


def test_equality(list1, list2):

    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
    
    return True


# constants
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.02
REPREDUCTION_RATE = 0.3

def generate_intial_population(size=8):
    population = []
    while len(population) != size:
        flag = 0
        member = [
                random.choice([0,1])
                for i in range(items)
                ]
        for members in population:
            if test_equality(member, members):
                flag = 1
                break
        if flag == 0:
            population.append(member)
    return population

def fitness(population):
    """
Fitness is evaluated as the sum of the values of the selected elements. 
In case the weight limit is exceeded, fitness for that member is set to 0. 
    """
    fitness_values = []
    for member in population:
        fitness_sum = 0
        weight_sum = 0
        for i in range(len(member)):  
            fitness_sum = fitness_sum + member[i]*values[i]
            weight_sum = weight_sum + member[i]*weights[i]
        if(weight_sum > limit):
            fitness_sum = 0
        fitness_values.append(fitness_sum)
    return fitness_values

def population_fitness_map(population, fitness_values):

    pop_fit_map = []
    for i in range(len(population)):
        pop_fit_map.append((population[i],fitness_values[i]))

    return pop_fit_map


def selection_of_candidates(candidates, first_member, second_member):
    if candidates[first_member][1] > candidates[second_member][1]:
        return first_member
    else:
        return second_member

def selection(candidates):
    """
Filters members suitable for reproduction. Filtering is done by manner of a tournament.
The list of members is split into 2, and one element from each half is taken. 
The one with higher fitness is selected, and both elements are popped from the list of candidates.
Process continues till the original list of candidates is exhausted, at which point the above is performed recursively.
The recursive operation stops when the desired number of candidates are selected (here, 2).
    """
    if len(candidates) == 2:
        return candidates

    selected_candidates = []
    iterations = len(candidates)//2
    
    #tournament 
    for i in range(iterations):
        first_member = random.randint(0,len(candidates)//2-1)
        second_member = random.randint(len(candidates)//2,len(candidates)-1)
        selected_member = selection_of_candidates(candidates, first_member, second_member)
        selected_candidates.append(candidates[selected_member])
        candidates.pop(second_member)
        candidates.pop(first_member)
    
    return selection(selected_candidates)

def crossover(parent):
    """
alleles are exchanged between the two parents by exchaning halves.
Input is a list of only the parent genes, not in a tuple with their fitnesses.
    """

    child1 = parent[1][:items//2] + parent[0][items//2:]
    child2 = parent[0][:items//2] + parent[1][items//2:]

    children = [child1,child2]
    return children

def mutation(parents):
    """
A bit is flipped randomly according to the mutation rate
    """
    for parent in parents:
        for i in range(len(parent)):
            if random.random() < MUTATION_RATE:
                bit = lambda bit: 0 if bit == 1 else 1
                parent[i] = bit(parent[i])

    return parents


def next_generation(population):

    next_gen = []

    while len(next_gen) < len(population):
        children = []
        fitness_values = fitness(population)
        fit_pop_map = population_fitness_map(population,fitness_values)
        parents_fitness_map = selection(fit_pop_map)
        parents = [parent[0] for parent in parents_fitness_map]
        if random.random() < REPREDUCTION_RATE:
            children = parents
        if random.random() < CROSSOVER_RATE:
            children = crossover(parents)
        if random.random() < MUTATION_RATE:
            children = mutation(children)

        next_gen.extend(children)

    return next_gen[:len(population)]

def solve_knapsack():
    population = generate_intial_population()
    average_fitness = []
    
    for i in range(5000):
        average_fitness_value = sum(fitness(population))/len(population)
        population = next_generation(population)
        average_fitness.append(average_fitness_value)

    genetic_data = {}
    genetic_data["top_fitness"] = max(average_fitness)
    genetic_data["average_fitnesses"] = average_fitness
    genetic_data["best_population"] = population
    return genetic_data

def main(request):
    global weights, values, limit, items
    weights = request.weights
    values = request.values
    limit = request.limit
    items = request.items

    solution = solve_knapsack()
    return solution
    # print(solution[1])



    

