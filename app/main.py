import time
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import random
import psycopg2
# from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    public: bool = True
    rating: Optional[int]
    post_id = random.randint(0, 9999999)


# Connect to database
for i in range(3):
    try:
        conn = psycopg2.connect(host='localhost', database='fast_api_tutorial', user='postgres',
                                password='')
        cursor = conn.cursor()
        print("Connection was successfull")
        break
    except Exception as error:
        print("Connection failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "hellow world"}


@app.get("/posts")
def get_posts():
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("select * from posts where post_id = (%s)", str(post_id))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {post_id} was not found")
    else:
        return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def make_post(post: Post):
    post_dict = post.dict()
    cursor.execute("""insert into posts (post_id, title, content, public)
                    values (%(post_id)s, %(title)s, %(content)s, %(public)s)
                    returning *""",
                   {"post_id": post.post_id, "title": post.title, "content": post.content, "public": post.public})
    cursor.fetchone()
    conn.commit()
    return {"post_data": post_dict}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    try:
        cursor.execute("delete from posts where post_id = %s returning *", str(post_id))
        cursor.fetchone()
        conn.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {post_id} not found")


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    try:
        cursor.execute("""update posts set
                            content = %(content)s, title = %(title)s, public = %(public)s returning *""",
                       {"content": post.content, "title": post.title, "public": post.public})
        cursor.fetchone()
        conn.commit()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {post_id} not found")
    else:
        return {"updated data": ""}
