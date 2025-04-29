import asyncio

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, constr

from app.database import get_connection, setup_db

app = FastAPI()


class User(BaseModel):
    name: str
    age: int


class UserCreate(BaseModel):
    name: constr(min_length=1)


def get_db():
    conn = get_connection()
    setup_db(conn)
    return conn


@app.get("/slow")
async def slow_response():
    await asyncio.sleep(1)
    return {"status": "ok", "response": "That was slow..."}


@app.get('/hello')
async def say_hello():
    await asyncio.sleep(1)
    return {"message": "Hello World!"}


@app.post("/users")
def create_user(user: UserCreate, conn=Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name) VALUES (%s) RETURNING id",
        (user.name,)
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    return {"status": "created", "id": user_id, "name": user.name}


@app.get("/users")
def list_users(conn=Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()
    return [{"id": row[0], "name": row[1]} for row in users]


@app.get("/users/{user_id}")
def get_user(user_id: int, conn=Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "name": row[1]}


@app.delete("/users/{user_id}")
def delete_user(user_id: int, conn=Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
    deleted = cursor.fetchone()
    conn.commit()
    if deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "deleted", "id": user_id}

