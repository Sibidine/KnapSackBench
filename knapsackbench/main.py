from fastapi import FastAPI, status, HTTPException
from algorithms import genetic_knapsack, simulated_annealing_knapsack, ant_colony_knapsack

app = FastAPI()

@app.get('/genetic', status_code=status.HTTP_200_OK)
def genetic():
    return genetic_knapsack.solve_knapsack()

@app.get('/simulated_annealing', status_code=status.HTTP_200_OK)
def SA():
    return simulated_annealing_knapsack.simulated_annealing()

@app.get('/ant_colony', status_code=status.HTTP_200_OK)
def ACO():
    return ant_colony_knapsack.main()
