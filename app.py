from flask import Flask, render_template, request, jsonify, redirect
import csv
import random
import string
import os
from urllib.parse import urlparse

app = Flask(__name__)

# CSV file path
CSV_FILE = 'urls.csv'

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sl_no', 'original_url', 'short_code'])

def generate_short_code():
    # Generate a 6-character random string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def is_valid_url(url):
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        
        # Check if URL has a valid domain with at least one dot and valid TLD
        domain_parts = result.netloc.split('.')
        if len(domain_parts) < 2:
            return False
        
        # List of common TLDs
        valid_tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil', 'in', 'co', 'io', 'app', 'dev']
        tld = domain_parts[-1].lower()
        
        return tld in valid_tlds
    except:
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if not is_valid_url(url):
        return jsonify({'error': 'Invalid URL format. Please enter a valid URL with a proper domain (e.g., https://example.com)'}), 400

    # Ensure CSV exists
    ensure_csv_exists()

    # Generate short code
    short_code = generate_short_code()

    # Read existing URLs to get next SL number
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        urls = list(reader)
        next_sl = len(urls) + 1

    # Add new URL to CSV
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([next_sl, url, short_code])

    return jsonify({
        'success': True,
        'short_code': short_code
    })

@app.route('/urls')
def get_urls():
    ensure_csv_exists()
    urls = []
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        urls = list(reader)
    
    if not urls:
        return jsonify({
            'message': 'No URLs exist. Create one above.',
            'urls': []
        })
    
    return jsonify(urls)

@app.route('/delete/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    try:
        ensure_csv_exists()
        
        # Read all URLs
        with open(CSV_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            urls = list(reader)
        
        # Find and remove the URL with matching short_code
        original_length = len(urls)
        urls = [url for url in urls if url[2] != short_code]
        
        # Check if URL was found and removed
        if len(urls) == original_length:
            return jsonify({'success': False, 'error': 'URL not found'}), 404
        
        # Create a temporary file
        temp_file = CSV_FILE + '.tmp'
        
        try:
            # Write to temporary file first
            with open(temp_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(urls)
            
            # If successful, replace the original file
            if os.path.exists(temp_file):
                if os.path.exists(CSV_FILE):
                    os.remove(CSV_FILE)
                os.rename(temp_file, CSV_FILE)
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Failed to update file'}), 500
                
        except Exception as e:
            # Clean up temporary file if it exists
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise e
            
    except Exception as e:
        print(f"Error deleting URL: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to delete URL'}), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    ensure_csv_exists()
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['short_code'] == short_code:
                return redirect(row['original_url'])
    return render_template('index.html'), 404

if __name__ == '__main__':
    ensure_csv_exists()
    app.run(debug=True) 