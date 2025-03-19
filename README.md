URL Shortener

A simple, lightweight, and efficient URL shortener built with Python. This project includes Gunicorn functionality for better performance and deployment.

Features

Shorten long URLs

Retrieve original URLs from shortened links

Simple and fast API

Open-source and customizable

Installation

Clone the repository:

git clone https://github.com/celicular/urlGen.git
cd urlGen

Install dependencies:

pip install -r requirements.txt

Usage

Run the application locally:

python app.py

Run with Gunicorn for better performance:

gunicorn -w 4 -b 0.0.0.0:8000 app:app

API Endpoints

POST /shorten – Shortens a given URL.

GET /<short_code> – Redirects to the original URL.

Deployment

You can deploy this project on platforms like Heroku, AWS, or DigitalOcean.

Example deployment using Gunicorn and systemd:

sudo cp url-shortener.service /etc/systemd/system/
sudo systemctl start url-shortener
sudo systemctl enable url-shortener

Contributing

Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

License

This project is open-source under the MIT License. Feel free to use and modify it as needed.

Credits

Developed by [Himadri Shekhar]. Please give proper credit when using or modifying this project.
