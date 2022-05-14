import re
from fastapi import Body, FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class UpdatePost(BaseModel):
    id: int
    title: str
    content: str
    pusblished: bool = False
    rating: Optional[float] = None


class Post(BaseModel):
    title: str
    content: str
    pusblished: bool = False
    rating: Optional[float] = None


my_posts = [
    {
        "title": "title of 1",
        "content": "content of 1",
        "id": 1
    },
    {
        "title": "title of 2",
        "content": "content of 2",
        "id": 2
    },
]


def find_post(id):
    for data in my_posts:
        if data["id"] == id:
            return data


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def read_root():
    return {"message": " Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/lastest")
def get_posts_by_id():
    post = my_posts[len(my_posts)-1]
    return {"data": post}


@app.get("/posts/{id}")
def get_posts_by_id(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with {id} was not found",)

    return {"data": post}


@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post, ):
    post_id = new_post.dict()
    post_id['id'] = randrange(0, 9999999999)
    my_posts.append(post_id)
    return {"message": post_id}


@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def detete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with {id} does not exist",)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/post/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with {id} does not exist",)

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": "updated post", "data": post}
