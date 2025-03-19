# 🌐 URL Shortener

![GitHub Repo Stars](https://img.shields.io/github/stars/celicular/urlGen?style=social)
![GitHub License](https://img.shields.io/github/license/celicular/urlGen)
![GitHub Issues](https://img.shields.io/github/issues/celicular/urlGen)
![GitHub Forks](https://img.shields.io/github/forks/celicular/urlGen)

A simple, lightweight, and efficient **URL shortener** built with Python. This project includes **Gunicorn** functionality for better performance and deployment.

---

## 📌 Table of Contents
- [🚀 Features](#-features)
- [🛠 Installation & Usage](#-installation--usage)
- [🔗 API Endpoints](#-api-endpoints)
- [🌍 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [✨ Credits](#-credits)
- [📂 Repository](#-repository)

---

## 🚀 Features

✅ Shorten long URLs  
✅ Retrieve original URLs from shortened links  
✅ Simple and fast API  
✅ Open-source and customizable  

---

## 🛠 Installation & Usage

### 1️⃣ Clone the Repository:
```bash
git clone https://github.com/celicular/urlGen.git
cd urlGen
 2️⃣ Install Dependencies:
bash
Copy code
pip install -r requirements.txt
3️⃣ Run the Application:
bash
Copy code
python app.py
4️⃣ Run with Gunicorn (for better performance):
bash
Copy code
gunicorn -w 4 -b 0.0.0.0:8000 app:app
🔗 API Endpoints
Method	Endpoint	Description
POST	/shorten	Shortens a given URL
GET	/<short_code>	Redirects to the original URL
🌍 Deployment
You can deploy this project on Heroku, AWS, DigitalOcean, or any cloud service.

Deploy with systemd:
bash
Copy code
sudo cp urlGen.service /etc/systemd/system/
sudo systemctl start urlGen
sudo systemctl enable urlGen
🤝 Contributing
💡 Contributions are welcome!
Feel free to fork the repository, make improvements, and submit a pull request.

Fork the repository
Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -m "Added a cool feature")
Push to the branch (git push origin feature-branch)
Open a Pull Request
📜 License
This project is open-source under the MIT License. Feel free to use and modify it as needed.

✨ Credits
Developed by Himadri. Please provide proper credit when using or modifying this project.
