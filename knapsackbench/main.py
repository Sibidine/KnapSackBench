from fastapi import FastAPI, status, HTTPException
from algorithms import genetic_knapsack, simulated_annealing_knapsack, ant_colony_knapsack
import models


app = FastAPI()

@app.post('/genetic', status_code=status.HTTP_200_OK)
def genetic(request: models.Constraints):
    response =  genetic_knapsack.solve_knapsack()
    return response

@app.post('/simulated_annealing', status_code=status.HTTP_200_OK)
def simulated_annealing(request: models.Constraints):
    respone =  simulated_annealing_knapsack.simulated_annealing()
    return response

@app.post('/ant_colony', status_code=status.HTTP_200_OK)
def ant_colony(request: models.Constraints):
    response =  ant_colony_knapsack.main()
    return response
