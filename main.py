from fastapi import FastAPI
# help(FastAPI) - > to see documentation of FastAPI
app = FastAPI() # create an instance of FastAPI

@app.get("/") # decorator to define a path
def root():
    return {"message": "Welcome back to my API!!!"} # return a dictionary

@app.get("/posts") # decorator to define a path
def get_posts():
    return {"data": "These are the posts"}