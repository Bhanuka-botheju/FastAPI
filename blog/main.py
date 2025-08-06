from typing import List
from fastapi import FastAPI,Depends,status, Response ,HTTPException
from . import schemas
from . import models
from . database import engine , SessionLocal
from sqlalchemy.orm import Session
from . import hashing

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

@app.get('/blog',status_code = 200 , response_model=List[schemas.ShowBlog])
async def get_blogs_all(db:Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK,response_model = schemas.ShowBlog )
async def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog_by_id = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    return blog_by_id

@app.post('/user',status_code = 200 )
async def create_user(request:schemas.User , db:Session = Depends(get_db)):
    exist_user = db.query(models.User).filter(models.User.email == request.email).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists log in...")
    hashedpassword = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name = request.name , email=request.email , password=hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',status_code = 200 , response_model = List[schemas.ShowUser])
async def get_all_users(db:Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return all_users

