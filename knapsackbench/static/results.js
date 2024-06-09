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
        } else {
            const responseDiv = document.createElement('div');
            responseDiv.classList.add('response');
            responseDiv.innerHTML = `<h3>${algorithm}</h3><pre>${JSON.stringify(result, null, 2)}</pre>`;
            resultsContainer.appendChild(responseDiv);
        }
    }
});
