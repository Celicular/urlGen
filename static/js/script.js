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

    // Function to strip URL protocol if exists
    function stripURLProtocol(url) {
        return url.replace(/^(https?:\/\/)?(www\.)?/, '');
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
            errorMessage.textContent = 'Please enter a valid URL';
            return;
        }

        // Strip protocol and www if exists
        const strippedURL = stripURLProtocol(urlToCheck);
        
        // Alert the stripped URL (this will be replaced with actual API call later)
        alert('Processed URL: ' + strippedURL);
    }

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
}); 