from symtable import Class
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/items")
async def items(limits:int ,published:bool , sort:Optional[str]=None):
    if(published):
        return {"message": f"Items with limits {limits} are published"}
    else:
        return {"message": f"Items with limits {limits} are not published"}    


@app.get("/about/{id}")
async def read_about(id):
    return {"message": id}

@app.get('/about/{id}/comments')
async def read_comments(id , limit: int = 10):
    return {"message": f"Comments for {id}"}


class Blog(BaseModel):
    title: str
    body: str
    published:Optional[bool]




@app.post("/blog")
async def create_blog(request : Blog):
    return {"masssege" : f'blog with title {request.title} and body {request.body} is created'}




