from fastapi import FastAPI
from . import schemas
from . import models
from . database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/blog")
async def create_blog(request: schemas.Blog):
    return {'title': request.title, 'content': request.content}