from fastapi import FastAPI
from . import schemas

app = FastAPI()



@app.post("/blog")
async def create_blog(request: schemas.Blog):
    return {'title': request.title, 'content': request.content}