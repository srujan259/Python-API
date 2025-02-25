from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2 # to connect to the database
from psycopg2.extras import RealDictCursor # to return data as dictionary
import time
from . import models
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import engine, get_db

# help(FastAPI) - > to see documentation of FastAPI
models.Base.metadata.create_all(bind=engine)

app = FastAPI() # create an instance of FastAPI



class Post(BaseModel): # define a class, Post, that inherits from BaseModel 
    title: str
    content: str
    published: bool = True # default value


while True:
    try:
        conn = psycopg2.connect(
            database="fastapi",
            user="postgres",
            password="password123",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor() # create a cursor object
        print("Connected to database")
        break
    except Exception as error:
        time.sleep(2)
        print("Unable to connect to the database")
        print(error)


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None

my_posts = [{"title": "title of post 1", "content": "content of post", "id": 1}, {"title": "favourite foods", "content": "i like steak", "id": 2}] # list of dictionaries

@app.get("/") # decorator to define a path
def root():
    return {"message": "Welcome to my API!!!"} # return a dictionary


@app.get("/posts") # decorator to define a path
def get_posts(db: Session = Depends(get_db)): # db is an instance of Session
    # cursor.execute("""SELECT * FROM posts;""") # execute a query
    # posts = cursor.fetchall() # fetch all the results
    posts = db.query(models.Post).all()
    return {"data": posts} # return a dictionary

@app.post("/posts", status_code=status.HTTP_201_CREATED) # decorator to define a path
def create_posts(post: Post, db: Session = Depends(get_db)): # post is an instance of Post
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)) # execute a query
    # new_post = cursor.fetchone() # fetch the result
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post} # return a dictionary
# title str, content str

@app.get("/posts/{id}") # decorator to define a path
def get_post(id: int, db: Session = Depends(get_db)): # id is an integer
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return {"post_detail": post} # return a dictionary  

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    db.commit()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)
    return {"data": existing_post} # return a dictionary
