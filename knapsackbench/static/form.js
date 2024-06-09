document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('optimizationForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const weights = document.getElementById('weights').value.split(',').map(Number);
        const values = document.getElementById('values').value.split(',').map(Number);
        const limit = parseInt(document.getElementById('limit').value);
        const items = weights.length;

        if (weights.length !== values.length) {
            alert('The number of elements in weights and values must be the same.');
            return;
        }

        const selectedAlgorithms = ['genetic', 'simulated_annealing', 'ant_colony', 'particle_swarm']

        const data = {
            weights: weights,
            values: values,
            limit: limit,
            items: items,
            algorithms: selectedAlgorithms
        };

        // Store data in local storage and navigate to results page
        localStorage.setItem('optimizationData', JSON.stringify(data));
        window.location.href = 'results.html';
    });

    document.getElementById('weights').addEventListener('input', updateItemsCount);
    document.getElementById('values').addEventListener('input', updateItemsCount);

    function updateItemsCount() {
        const weights = document.getElementById('weights').value.split(',').map(Number);
        const values = document.getElementById('values').value.split(',').map(Number);

        if (weights.length === values.length) {
            document.getElementById('items').value = weights.length;
        } else {
            document.getElementById('items').value = '';
        }
    }
});
