# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
#def home():
   # return "Welcome to OpenHAMSv8"

#if __name__ == '__main__':
  #  app.run(debug=True)


import uvicorn
from .app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)