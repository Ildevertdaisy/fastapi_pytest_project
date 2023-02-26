
from fastapi import FastAPI, status
from pydantic import BaseModel


app = FastAPI()

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


@app.get("/")
async def hello_world():
    return {"hello": "world"}


@app.post("/persons", status_code=status.HTTP_201_CREATED)
async def create_person(person: Person):
    return person


@app.on_event("startup")
async def startup():
    print("Startup")


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown")