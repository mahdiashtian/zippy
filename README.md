# Zippy

# Overview

Zippy is a small Chatroom project written using Fast API, uses HTTP and WebSocket protocols, and its authentication is
in the form of JWT tokens.
It uses Postegras as a database, but it is possible that MongoDB will be added to it soon

# Features

- [x] HTTP and WebSocket protocols : It uses the HTTP protocol to manage users and rooms and the Websocket protocol to
  communicate between clients.
- [x] Database Integration : It uses SqlAlchemy for database management, which allows you to use other databases such as
  MySQL without the need for major changes in the code.
- [x] JWT Authentication : It uses JWT tokens to authenticate users, which works on platforms other than the web
- [x] Clear structure : The code is written in a way that is easy to understand and modify

# Getting Started

## Requirements

- Python 3.8 and above
- Postegras or any other database supported by SqlAlchemy

## Installation

1. Clone the repository<br/>
   ```git clone https://github.com/mahdiashtian/zippy.git```
2. Navigate to the project directory<br/>
   ```cd zippy```
3. Create and activate a virtual environment<br/>
    1. ```sudo apt install python3.10-venv``` (Linux)
    2. ```python -m venv venv```
    3. ```source venv/bin/activate``` (Linux)
       ```venv\Scripts\activate``` (Windows)
4. Install the requirements<br/>
   ```pip install -r requirements.txt```
5. Fixed imports<br/>
   ```pip install -e .```

## Configuration
To launch the project, you need to replace your project settings in the .env file with the default settings.
Required values:
```
SECRET_KEY=''
PSQL_DATABASE_USER=''
PSQL_DATABASE_PASSWORD=''
PSQL_DATABASE_NAME=''
PSQL_DATABASE_HOST=''
```

## Usage
Start the server<br/>
```python src/main.py```<br/>
launch up this project is very easy and does not require any other settings

# Contact
For any questions or suggestions, please contact [me](mailto:mahdiashtian.mo@gmail.com)
