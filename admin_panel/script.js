document.addEventListener('DOMContentLoaded', function() {
    const logsContainer = document.querySelector('.logs-container');
    const logsPre = logsContainer ? logsContainer.querySelector('pre') : null;

    if (!logsContainer || !logsPre) return;

    // Function to fetch logs
    function fetchLogs() {
        fetch('get_logs.php')
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.text();
            })
            .then(data => {
                // Only update if content has changed
                if (logsPre.textContent !== data) {
                    // Check if user is near the bottom (within 50px) before updating
                    const isAtBottom = logsContainer.scrollHeight - logsContainer.scrollTop - logsContainer.clientHeight < 50;
                    
                    logsPre.textContent = data;

                    // If user was at bottom, auto-scroll to new bottom
                    if (isAtBottom) {
                        logsContainer.scrollTop = logsContainer.scrollHeight;
                    }
                }
            })
            .catch(error => console.error('Error fetching logs:', error));
    }

    // Poll every 3 seconds
    setInterval(fetchLogs, 1000);
    
    // Scroll to bottom on initial load
    logsContainer.scrollTop = logsContainer.scrollHeight;

    // --- CHARTS INITIALIZATION ---
    if (window.chartData) {
        const data = window.chartData;

        // 1. Usage Chart (Line)
        const ctxUsage = document.getElementById('usageChart').getContext('2d');
        new Chart(ctxUsage, {
            type: 'line',
            data: {
                labels: data.dates,
                datasets: [{
                    label: 'Podcasts Generated',
                    data: data.counts,
                    borderColor: '#1877f2',
                    backgroundColor: 'rgba(24, 119, 242, 0.1)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { title: { display: true, text: 'Daily Usage' } },
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
            }
        });

        // 2. Cities Chart (Bar)
        const ctxCities = document.getElementById('citiesChart').getContext('2d');
        new Chart(ctxCities, {
            type: 'bar',
            data: {
                labels: data.cities,
                datasets: [{
                    label: 'Requests',
                    data: data.city_counts,
                    backgroundColor: '#42b72a'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { title: { display: true, text: 'Top Cities' } }
            }
        });

        // 3. Topics Chart (Doughnut)
        const ctxTopics = document.getElementById('topicsChart').getContext('2d');
        new Chart(ctxTopics, {
            type: 'doughnut',
            data: {
                labels: data.topics,
                datasets: [{
                    data: data.topic_counts,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { title: { display: true, text: 'Popular Interests' } }
            }
        });
    }
});