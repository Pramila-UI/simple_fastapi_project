from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()  # load the .env file

app = FastAPI()

from .apis import *

@app.get('/')
def home_page():
    return {
        "status" : "success" ,
        "message" : "Running Successfully"
    }

