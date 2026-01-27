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
});