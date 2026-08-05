from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string

app = FastAPI()
@app.get("/")
def home():
    return{"message":"Welcome to URL shortener Api"
        }

@app.get("/about")
def ab():
    return {"Project":"Url shorterner",
    "Author":"Adi"
    }   
@app.get("/hello/{name}")
def greet(name):
    return {"Message":f"Heloow {name}",
    "message":"Welcome!",
    "original": name,
    "uppercase": name.upper(),
    "lowercase": name.lower(),
    "lenght":len(name),
    "first_letter": name[0],
  "last_letter": name[-1],
  "reversed": name[::-1]
    } 

@app.get("/search")
def search(q):
    return{
        "query":q
    }

@app.get("/calculator")
def calculate(a:int,b:int):
    return {
        "a": a,
        "b": b,
        "sum":a + b
    }

class URLRequest(BaseModel):
    url : str


url_database = {}

@app.post("/shorten")
def shorten(request: URLRequest):
    short_code = generate_short_code()
    url_database[short_code] = request.url

    print(url_database)

    return {
        "originalUrl": request.url,
        "shortcode": short_code
    }

@app.get("/code/{code}")
def redirect(code:str):
    if code in url_database:
        return {"originalURL":url_database[code]
        }
    raise HTTPException(
    status_code=404,
    detail="Short code not found"
)

def generate_short_code(length=6):
    res = ""
    chars = string.digits+string.ascii_letters
    while True:
        res = ""
        for i in range(length):
            res+=random.choice(chars)
        if res not in url_database:
           return res