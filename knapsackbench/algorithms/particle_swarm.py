import random

# contraints

weights = []
values = []
limit =  0
items = 0

# constants

no_of_particles = 50
omega = 0.729
alpha = 1.9
beta = 1.1
iterations = 100

def fitness(particle):
    """
    Fitness is given by the sum of values picked for the particle.
    Fitness is 0 if weight limit is exceeded.
    """

    sum_values = 0
    sum_weights = 0
    for i in range(len(particle)):
        
        if particle[i] == 1:
            sum_values += values[i]
            sum_weights += weights[i]
            

    if sum_weights > limit:
        sum_values = 0
    return sum_values


def xor(list_1, list_2):

    return  list(a^b for a,b in zip(list_1, list_2))


def initialise_particles():
    """
    initialises each particle to a random position and velocity list
    """

    list_of_particles = []
    for i in range(no_of_particles):

        fitness_of_position = 0
        while fitness_of_position == 0:
            position = [
                random.choice([0,1])
                for i in range(items)
            ]
            fitness_of_position = fitness(position)


        velocity = position = [
            random.choice([0,1])
            for i in range(items)
        ]

        list_of_particles.append([position, velocity]) 
    
    return list_of_particles


def normalised(velocity):
    """
    converts the decimal velocity into a binary string
    """
    best = max(velocity)
    for i in range(items):
        
        if velocity[i] >= best*0.5:
            velocity[i] = 1
        else:
            velocity[i] = 0
    return velocity

def flip(position):
    """
    flips a random bit in the position vector to avoid local maxima.
    """
    pos = random.randint(0, len(position)-1)

    if position[pos] == 1:
        position[pos] = 0
    else:
        position[pos] = 1
    return position


def find_velocity(position, velocity, Pbest, Gbest):
    """
    finds the velocity at the current iteration.
    """

    change_from_pbest = xor(position, Pbest)
    change_from_pbest = flip(change_from_pbest)
    change_from_pbest = [i*alpha for i in change_from_pbest]
    # print(change_from_pbest)
    change_from_gbest = xor(position, Gbest)
    change_from_gbest = [i*beta for i in change_from_gbest]

    new_velocity = [omega*i for i in velocity]
    
    for i in range(items):
        new_velocity[i] += change_from_gbest[i] + change_from_pbest[i]
    return normalised(new_velocity)


def max_Pbest(Pbest):
    """
    finds the best historically best position per particle
    """
    max_val = 0
    Gbest = []
    for key,value in Pbest.items():
        if max_val < value[1]:
            max_val = value[1]
            Gbest = value[0]
    
    return Gbest


def particle_swarm():

    particle = initialise_particles()
    # Pbest_config = [[]] * no_of_particles
    # Pbest_value = [0] * no_of_particles
    Pbest = {}
    for i in range(no_of_particles):
        Pbest[i] = (particle[i][0],0)
    Gbest = []
    historical_Gbest = []
    iteration_number = 0
    particle_swarm_data = {}
    while iteration_number < iterations:

        for i in range(no_of_particles):
            fitness_of_particle = fitness(particle[i][0])
            if fitness_of_particle > Pbest[i][1]:
                Pbest[i] = list(Pbest[i])
                Pbest[i][1] = fitness_of_particle
                Pbest[i][0] = particle[i][0]
                Pbest[i] = tuple(Pbest[i])
                
 
        Gbest = max_Pbest(Pbest)

        for i in range(no_of_particles):
            # print(particle[i][1])
            particle[i][1] = find_velocity(particle[i][0], particle[i][1], Pbest[i][0], Gbest)
            particle[i][0] = xor(particle[i][0], particle[i][1])
            
        
        iteration_number += 1
        historical_Gbest.append(fitness(Gbest))
    # print(historical_Gbest)
    particle_swarm_data["global_best_configuration"] = Gbest
    particle_swarm_data["global_best_value"] = fitness(Gbest)
    particle_swarm_data["historical_global_bests"] = historical_Gbest

    return particle_swarm_data


def main(request):

    global weights, values, limit, items

    weights = request.weights
    values = request.values
    limit = request.limit
    items = request.items

    return particle_swarm()


        
