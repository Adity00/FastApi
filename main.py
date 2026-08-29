from fastapi import FastAPI

from routes.urls import router

app = FastAPI()

@app.get("/")
def home():
    return{
        "message":"Welcome to URL shortener"
    }

@app.get("/about")
def ab():
    return{
        "Project":"URL shortener",
        "Author":"Adi"
    }

@app.get("/hello/{name}")
def greet(name:str):
    return{
        "Message":f"Hello{name}",
        "message": "Welcome!",
        "original": name,
        "uppercase": name.upper(),
        "lowercase": name.lower(),
        "length": len(name),
        "first_letter": name[0],
        "last_letter": name[-1],
        "reversed": name[::-1]
    }

@app.get("/search")
def search(q:str):
    return{
        "query":q
    }

@app.get("/calculator")
def calculate(a:int,  b:int):
    return{
        "a":a,
        "b":b,
        "sum":a+b
    }

app.include_router(router)