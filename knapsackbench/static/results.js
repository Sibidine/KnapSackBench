document.addEventListener('DOMContentLoaded', async function() {
    const data = JSON.parse(localStorage.getItem('optimizationData'));

    if (!data) {
        alert('No optimization data found.');
        window.location.href = 'index.html';
        return;
    }

    const { weights, values, limit, items, algorithms } = data;
    const endpoints = {
        genetic: 'http://localhost:8000/genetic',
        simulated_annealing: 'http://localhost:8000/simulated_annealing',
        ant_colony: 'http://localhost:8000/ant_colony',
        particle_swarm: 'http://localhost:8000/particle_swarm'
    };

    const resultsContainer = document.getElementById('responses');
    const topFitnessDiv = document.getElementById('top-fitness');
    const fitnessChartCanvas = document.getElementById('fitness-chart');
    const bestObjectiveDiv = document.getElementById('best-objective');
    const bestObjectiveCanvas = document.getElementById('best-objective-chart');
    const bestSolutionDiv = document.getElementById('best-solution');
    const bestSolutionCanvas = document.getElementById('best-solution-chart');
    const bestConfigDiv = document.getElementById('best-config');
    const bestConfigCanvas = document.getElementById('best-config-chart');
    
    
    
    for (const algorithm of algorithms) {
        const response = await fetch(endpoints[algorithm], {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ weights, values, limit, items })
        });
        const result = await response.json();
        displayResponse(algorithm, result);
    }

    function displayResponse(algorithm, result) {
        if (algorithm === 'genetic') {
            topFitnessDiv.textContent = `Top Fitness: ${result.top_fitness}`;

            const ctx = fitnessChartCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: result.average_fitnesses.map((_, index) => index + 1),
                    datasets: [{
                        label: 'Average Fitness',
                        data: result.average_fitnesses,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Generation'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Fitness'
                            }
                        }
                    }
                }
            });
        }
        else if (algorithm === 'simulated_annealing') {
            bestObjectiveDiv.textContent = `Best Objective: ${result.best_objective}`;

            const ctx = bestObjectiveCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: result.solutions_history.map((_, index) => index + 1),
                    datasets: [{
                        label: 'Average Objective Value',
                        data: result.solutions_history,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Generation'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Objective Value'
                            }
                        }
                    }
                }
            });
        } 
        else if (algorithm === 'ant_colony') {
            bestSolutionDiv.textContent = `Best Solution: ${result.max_profit}`;

            const ctx = bestSolutionCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: result.profit_history.map((_, index) => index + 1),
                    datasets: [{
                        label: 'Average Solution',
                        data: result.profit_history,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Generation'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Objective Value'
                            }
                        }
                    }
                }
            });
        }
        else if (algorithm === 'particle_swarm') {
            bestConfigDiv.textContent = `Best Configuration: ${result.global_best_value}`;

            const ctx = bestConfigCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: result.historical_global_bests.map((_, index) => index + 1),
                    datasets: [{
                        label: 'Average Solution',
                        data: result.historical_global_bests,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Generation'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Objective Value'
                            }
                        }
                    }
                }
            });
        }




        
        else {
            const responseDiv = document.createElement('div');
            responseDiv.classList.add('response');
            responseDiv.innerHTML = `<h3>${algorithm}</h3><pre>${JSON.stringify(result, null, 2)}</pre>`;
            resultsContainer.appendChild(responseDiv);
        }
    }
});
