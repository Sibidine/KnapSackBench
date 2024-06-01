from fastapi import FastAPI, status, HTTPException
from algorithms import genetic_knapsack, simulated_annealing_knapsack, ant_colony_knapsack, particle_swarm
import models


app = FastAPI()

@app.post('/genetic', status_code=status.HTTP_200_OK)
def genetic(request: models.Constraints):
    """
    Uses the Genetic Algorithm to find an optimised solution.
    
    Returned data:

    {

        top_fitness: float - the highest average fitness value of a generation obtained from execution.
        
        average_fitnesses: list(float) - a list of the average fitness values of each generation.
        
        best_population: list(list(int))- a list of lists of 100 binary integers, denoting the last population.
    }

    """
    response =  genetic_knapsack.main(request)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'detail': 'model under maintenance, please try again later'})
    return response

@app.post('/simulated_annealing', status_code=status.HTTP_200_OK)
def simulated_annealing(request: models.Constraints):
    """
    Uses the Simulated Annealing algorithm to find an optimised solution.
    
    Returned data:

    {

        improvements: int - a count of the number of numeric improvements in the objective function value.

        random_steps: int - a count of the number of random steps made away from a maximum according to the metropolis criterion.
        
        solutions_history: list(int) - a list of the best solutions checked per iteration.
        
        best_config: list(int) - a list of 100 binary integers denoting the optimised solution
        
        best_objective: int - the objective function value for the best configuration.
    }

    """
    response =  simulated_annealing_knapsack.main(request)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'detail': 'model under maintenance, please try again later'})
    return response

@app.post('/ant_colony', status_code=status.HTTP_200_OK)
def ant_colony(request: models.Constraints):
    """
    Uses Ant Colony Optimisation to find an optimised solution.
    
    Returned data:

    {

        max_profit: int - the highest value attained by optimisation
        
        profit_history: list(int) - a list of the best solutions found per iteration
        
        solution_set: list(int)- a list of 100 binary integers denoting the optimised solution
    }
    """
    response =  ant_colony_knapsack.main(request)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'detail': 'model under maintenance, please try again later'})
    return response

@app.post('/particle_swarm', status_code=status.HTTP_200_OK)
def particle_swarm(request: models.Constraints):
    """
    Uses Particle Swarm Optimisation to find an optimised solution.

    Returned data:

    {

        global_best_configuration: list(int) - a list of 100 binary integers denoting the optimal knapsack solution.

        global_best_value: int - the highest fitness value attained by the optimisation algorithm

        historical_global_bests: list(int) -  a list of the best fitness values for all particles attained at each iteration.
    }
    """
    response = particle_swarm.main()
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'detail': 'model under maintenance, please try again later'})
    return response