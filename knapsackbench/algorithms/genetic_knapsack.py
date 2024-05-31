import random

# contraints

weights = [21, 12, 30, 24, 45, 47, 41, 36, 38, 45, 4, 17, 1, 42, 26, 19, 12, 27, 15, 4, 5, 4, 21, 7, 23, 45, 18, 7, 29, 44, 18, 3, 8, 4, 38, 23, 34, 35, 29, 32, 44, 34, 44, 24, 8, 4, 36, 16, 34, 33, 27, 36, 26, 25, 25, 47, 20, 6, 13, 35, 42, 49, 11, 39, 30, 21, 26, 25, 33, 38, 16, 5, 42, 20, 39, 9, 6, 46, 44, 50, 44, 2, 28, 50, 26, 44, 4, 50, 47, 29, 22, 17, 37, 1, 19, 47, 28, 24, 25, 16]
values = [96, 99, 52, 100, 46, 43, 22, 20, 84, 73, 53, 83, 52, 56, 22, 59, 15, 6, 69, 61, 22, 41, 63, 56, 13, 17, 1, 42, 49, 16, 67, 2, 12, 96, 98, 4, 50, 87, 25, 84, 82, 63, 1, 38, 91, 69, 38, 64, 25, 58, 99, 85, 29, 69, 36, 99, 9, 26, 82, 9, 54, 81, 74, 15, 44, 36, 48, 59, 15, 91, 65, 17, 57, 94, 79, 69, 47, 27, 57, 25, 32, 92, 89, 80, 93, 18, 52, 63, 92, 67, 39, 75, 82, 61, 9, 93, 6, 53, 12, 39]
limit = 1500
items = len(weights)



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

def main():
    solution = solve_knapsack()
    print(solution["average_fitnesses"][4999])
    # print(solution[1])



    

