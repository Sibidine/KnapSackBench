# KnapSackBench

KnapSackBench utilises the [0-1 Knapsack Problem](https://en.wikipedia.org/wiki/Knapsack_problem) benchmarks the performance of various non-traditional optimisation algorithms-

- [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)
- [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
- [Ant Colony Optimisation](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)


Performance is measured by the total value evaluated under the given constraints by the various algorithms, with the higher value being better. Alongside this value, other metrics such as intermediate values and the solution configuration of items to pick are also provided for further analysis.

### Installation Instructions

```sh
git clone https://github.com/Sibidine/KnapSackBench.git
cd KnapSackBench 
```

Beyond this, it is recommended to use a virtual environment. The following commands may be considered for it:

```sh
pip install virtualenv
python -m venv knapsack-env
virtualenv knapsack-env
source knapsack-env/bin/activate
```

Beyond this, startup may be handled by `startup.sh`.

```sh
chmod +x startup.sh
./startup.sh
```
