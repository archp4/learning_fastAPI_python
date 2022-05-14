from fastapi import Body, FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    pusblished: bool = False
    rating: Optional[float] = None


@app.get("/")
def read_root():
    return {"message": " Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "This is Your Data"}


@app.post('/create_post')
def create_posts(new_post: Post):
    print(new_post.dict)
    return {"message": new_post}
