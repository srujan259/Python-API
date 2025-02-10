from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional

# help(FastAPI) - > to see documentation of FastAPI
app = FastAPI() # create an instance of FastAPI

class Post(BaseModel): # define a class, Post, that inherits from BaseModel 
    title: str
    content: str
    published: bool = True # default value
    rating: Optional[int] = None # optional value

@app.get("/") # decorator to define a path
def root():
    return {"message": "Welcome back to my API!!!"} # return a dictionary

@app.get("/posts") # decorator to define a path
def get_posts():
    return {"data": "These are the posts"}

@app.post("/createposts") # decorator to define a path
def create_posts(post: Post): # post is an instance of Post
    print(f"Title is {post.title}")
    print(f"Content is {post.content}")
    print(f"Published is {post.published}")
    print(f"Rating is {post.rating}")
    print(post.dict()) # convert to dictionary
    return {"data": post} # return a dictionary
# title str, content str