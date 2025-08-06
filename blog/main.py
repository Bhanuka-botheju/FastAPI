from fastapi import FastAPI,Depends
from . import schemas
from . import models
from . database import engine , SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog")
async def create_blog(request: schemas.Blog , db:Session = Depends(get_db)):
    new_blog = models.Blog(title =request.title, body=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog