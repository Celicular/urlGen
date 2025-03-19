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
        return all([result.scheme, result.netloc])
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
        return jsonify({'error': 'Invalid URL format'}), 400

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
    return jsonify(urls)

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