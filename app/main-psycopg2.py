from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2 # to connect to the database
from psycopg2.extras import RealDictCursor # to return data as dictionary
import time
from . import models
from .database import engine, SessionLocal

# help(FastAPI) - > to see documentation of FastAPI
models.Base.metadata.create_all(bind=engine)

app = FastAPI() # create an instance of FastAPI

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel): # define a class, Post, that inherits from BaseModel 
    title: str
    content: str
    published: bool = True # default value

while True:
    try:
        conn = psycopg2.connect(
            database="fastapi",
            user="postgres",
            password="Password@123",
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
    return {"message": "Welcome back to my API!!!"} # return a dictionary

@app.get("/posts") # decorator to define a path
def get_posts():
    cursor.execute("""SELECT * FROM posts;""") # execute a query
    posts = cursor.fetchall() # fetch all the results
    print(posts)
    # print(my_posts) # example to show the list of dictionaries from variable my_posts
    return {"data": posts} # return a dictionary

@app.post("/posts", status_code=status.HTTP_201_CREATED) # decorator to define a path
def create_posts(post: Post): # post is an instance of Post
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)) # execute a query
    new_post = cursor.fetchone() # fetch the result
    conn.commit()
    return {"data": new_post} # return a dictionary
# title str, content str

@app.get("/posts/{id}") # decorator to define a path
def get_post(id: int): # id is an integer
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),)) # execute a query
    post = cursor.fetchone() # fetch the result
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return {"post_detail": post} # return a dictionary  

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return {"data": updated_post}
