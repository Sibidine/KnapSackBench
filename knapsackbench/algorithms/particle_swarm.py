import random

# contraints

weights = [21, 12, 30, 24, 45, 47, 41, 36, 38, 45, 4, 17, 1, 42, 26, 19, 12, 27, 15, 4, 5, 4, 21, 7, 23, 45, 18, 7, 29, 44, 18, 3, 8, 4, 38, 23, 34, 35, 29, 32, 44, 34, 44, 24, 8, 4, 36, 16, 34, 33, 27, 36, 26, 25, 25, 47, 20, 6, 13, 35, 42, 49, 11, 39, 30, 21, 26, 25, 33, 38, 16, 5, 42, 20, 39, 9, 6, 46, 44, 50, 44, 2, 28, 50, 26, 44, 4, 50, 47, 29, 22, 17, 37, 1, 19, 47, 28, 24, 25, 16]
values = [96, 99, 52, 100, 46, 43, 22, 20, 84, 73, 53, 83, 52, 56, 22, 59, 15, 6, 69, 61, 22, 41, 63, 56, 13, 17, 1, 42, 49, 16, 67, 2, 12, 96, 98, 4, 50, 87, 25, 84, 82, 63, 1, 38, 91, 69, 38, 64, 25, 58, 99, 85, 29, 69, 36, 99, 9, 26, 82, 9, 54, 81, 74, 15, 44, 36, 48, 59, 15, 91, 65, 17, 57, 94, 79, 69, 47, 27, 57, 25, 32, 92, 89, 80, 93, 18, 52, 63, 92, 67, 39, 75, 82, 61, 9, 93, 6, 53, 12, 39]
limit = 1500
items = len(weights)

# constants

no_of_particles = 50
omega = 0.729
alpha = 1.49
beta = 1.49
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


def main():

    

    print(particle_swarm()["global_best_value"])


main()

        
