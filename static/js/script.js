// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('urlInput');
    const generateBtn = document.getElementById('generateBtn');
    const errorMessage = document.getElementById('errorMessage');

    // Function to validate URL
    function isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }

    // Function to handle URL generation
    function handleURLGeneration() {
        const inputValue = urlInput.value.trim();
        
        // Clear previous error
        errorMessage.textContent = '';
        
        // Check if input is empty
        if (!inputValue) {
            errorMessage.textContent = 'Please enter a URL';
            return;
        }

        // Add https:// if no protocol is specified
        let urlToCheck = inputValue;
        if (!urlToCheck.startsWith('http://') && !urlToCheck.startsWith('https://')) {
            urlToCheck = 'https://' + urlToCheck;
        }

        // Validate URL
        if (!isValidURL(urlToCheck)) {
            errorMessage.textContent = 'Please enter a valid URL (e.g., https://example.com)';
            return;
        }

        // Send URL to backend
        fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: urlToCheck })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorMessage.textContent = data.error;
                return;
            }
            // Clear input
            urlInput.value = '';
            // Refresh the table
            loadURLHistory();
        })
        .catch(error => {
            errorMessage.textContent = 'An error occurred. Please try again.';
        });
    }

    // Function to load URL history
    function loadURLHistory() {
        fetch('/urls')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('tbody');
            tbody.innerHTML = '';
            
            data.forEach((item, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td class="url-cell">${item.original_url}</td>
                    <td class="url-cell">${window.location.origin}/${item.short_code}</td>
                    <td class="action-cell">
                        <button class="action-btn copy-btn" title="Copy" onclick="copyToClipboard('${window.location.origin}/${item.short_code}')">
                            <i class="fas fa-copy"></i>
                        </button>
                        <a href="${window.location.origin}/${item.short_code}" class="action-btn visit-btn" title="Visit" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                        </a>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error loading URL history:', error);
        });
    }

    // Function to copy to clipboard
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert('URL copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    };

    // Add click event listener to the generate button
    generateBtn.addEventListener('click', function(e) {
        e.preventDefault();
        handleURLGeneration();
    });

    // Add enter key press listener to the input field
    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleURLGeneration();
        }
    });

    // Add input event listener to clear error message when user starts typing
    urlInput.addEventListener('input', function() {
        errorMessage.textContent = '';
    });

    // Load URL history when page loads
    loadURLHistory();
}); 