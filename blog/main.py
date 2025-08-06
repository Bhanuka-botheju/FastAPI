from fastapi import FastAPI,Depends,status, Response ,HTTPException
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

@app.post("/blog",status_code =status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog , db:Session = Depends(get_db)):
    new_blog = models.Blog(title =request.title, body=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_by_id(id , db:Session = Depends(get_db)):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.delete(blog_by_id)
    db.commit()
    return {"detail": f"Blog with id {id} deleted successfully"}

@app.put('/blog/{id}' , status_code=status.HTTP_202_ACCEPTED)
async def update_by_id(id,request:schemas.Blog , db:Session = Depends(get_db)):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog_by_id.title = "updated title"
    blog_by_id.body = "updated body"
    db.commit()
    db.refresh(blog_by_id)
    return blog_by_id

@app.get('/blog')
async def get_blogs_all(db:Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

@app.get('/blog/{id}')
async def get_blog_by_id(id, response:Response, db:Session = Depends(get_db),status_code=200):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
    return blog_by_id