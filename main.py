from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/about/{id}")
async def read_about(id):
    return {"message": id}

@app.get('/about/{id}/comments')
async def read_comments(id):
    return {"message": f"Comments for {id}"}

