from fastapi import FastAPI

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