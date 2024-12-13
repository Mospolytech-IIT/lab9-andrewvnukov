from fastapi import FastAPI, Depends, HTTPException, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import declarative_base, sessionmaker, Session  # Для SQLAlchemy
from database import SessionLocal, engine, User, Post, add_user, add_post, get_all_users, get_all_posts, update_user, update_post, delete_user, delete_post, get_user, get_post

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    users = get_all_users()
    posts = get_all_posts()
    return templates.TemplateResponse("index.html", {"request": request, "users": users, "posts": posts})

@app.post("/add_user", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_new_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_id = add_user(username, email, password)
    if user_id:
        return get_user(user_id)
    else:
        raise HTTPException(status_code=400, detail="Error adding user (duplicate?)")

@app.post("/add_post", response_model=Post, status_code=status.HTTP_201_CREATED)
async def add_new_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    post_id = add_post(title, content, user_id)
    if post_id:
        return get_post(post_id)
    else:
        raise HTTPException(status_code=400, detail="Error adding post")

@app.put("/update_user/{user_id}", response_model=User)
async def update_user_route(user_id: int, username: str = Form(None), email: str = Form(None), password: str = Form(None), db: Session = Depends(get_db)):
    success = update_user(user_id, username, email, password)
    if success:
        return get_user(user_id)
    else:
        raise HTTPException(status_code=400, detail="Error updating user")

@app.put("/update_post/{post_id}", response_model=Post)
async def update_post_route(post_id: int, title: str = Form(None), content: str = Form(None), db: Session = Depends(get_db)):
    success = update_post(post_id, title, content)
    if success:
        return get_post(post_id)
    else:
        raise HTTPException(status_code=400, detail="Error updating post")

@app.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(user_id)
    if success:
        return
    else:
        raise HTTPException(status_code=400, detail="Error deleting user")

@app.delete("/delete_post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_route(post_id: int, db: Session = Depends(get_db)):
    success = delete_post(post_id)
    if success:
        return
    else:
        raise HTTPException(status_code=400, detail="Error deleting post")
