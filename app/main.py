from fastapi import FastAPI,Response,HTTPException,status
import uvicorn
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

# while True:    
try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='123456',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesful!")
except Exception as error:
    print("Connecting to database failed!")
    print("Error was: ", error)
    time.sleep(2)

my_posts = [{"title": "title 1","content": "content 1", "id":1},{"title":"title 2","content": "content2", "id":2}]
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
def find_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    conn.commit()
    new_post = cursor.fetchone()
    return {"data": new_post}

@app.get("/posts/latest")
def get_latest_post():
    l = len(my_posts)-1
    print(type(l))
    latst = my_posts[l]
    return {"latest": latst}

@app.get("/posts/{id}")
def get_post(id: int, response = Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    post_finded = find_post(id)
    if not post:
       raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"id {id} is not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {"message": f"post with {id} id was not found"}
    return {"post": post}
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index(id)   
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)), )        
    deleted_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} doesnot exist")     
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    idx = find_index(id)
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" post with id: {id} doesnot exist")     
    
    return {"messsage": updated_post}

if __name__=="__main__":
    uvicorn.run(app)
