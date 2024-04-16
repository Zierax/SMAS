<h1 align="center">
  <img src="src/logo.smas.png" alt="smass" width="200px">
  <br>
  SMAS
</h1>
<h4 align="center">SQL Injection scanner made with Python.</h4>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#running-smas">Usage</a> •
  <a href="#license">License</a>
</p>

SMAS (SQL Injection Made Simple) is an efficient SQL injection scanner crafted in Python. It excels at detecting GET-based SQL injection vulnerabilities within web applications by leveraging a blend of waybackurls, web crawlers, and SQL injection payloads.


Features
<h1 align="center">
</h1>
Fast and efficient scanner
Includes web crawler and waybackurls for comprehensive scanning
Installation
SMAS requires the following dependencies:

Python 3
huepy
requests
tqdm
To install SMAS, follow these steps:

sh
Copy code
▶ sudo apt install git
sh
Copy code
▶ git clone https://github.com/Zierax/SMAS
sh
Copy code
▶ cd smas
▶ pip3 install -r requirements.txt
Running SMAS
To run SMAS on a target, use the following command:

sh
Copy code
▶ python3 smas.py -d example.com
You can also use the -s option to test SQL injection on subdomains of the target:

sh
Copy code
▶ python3 smas.py -d example.com -s
License
SMAS is made by Zierax with MIT licenses. You can find me on Twitter and GitHub.