import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session  # Для SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

DATABASE_URL = "mysql://root:1234567890Aa@localhost:3306/testbase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def add_user(username, email, password):
    with Session() as session:
        new_user = User(username=username, email=email, password=password)
        try:
            session.add(new_user)
            session.commit()
            return new_user.id
        except IntegrityError as e:
            session.rollback()
            print(f"Error adding user: {e}")
            return None

def add_post(title, content, user_id):
    with Session() as session:
        new_post = Post(title=title, content=content, user_id=user_id)
        session.add(new_post)
        session.commit()
        return new_post.id

def get_all_users():
    with Session() as session:
        return session.query(User).all()

def get_all_posts():
    with Session() as session:
        return session.query(Post).all()

def get_posts_by_user(user_id):
    with Session() as session:
        return session.query(Post).filter(Post.user_id == user_id).all()

def get_user(user_id):
    with Session() as session:
        return session.query(User).get(user_id)

def get_post(post_id):
    with Session() as session:
        return session.query(Post).get(post_id)

def update_user(user_id, username=None, email=None, password=None):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            if username: user.username = username
            if email: user.email = email
            if password: user.password = password
            try:
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error updating user: {e}")
                return False
        return False

def update_post(post_id, title=None, content=None):
    with Session() as session:
        post = session.query(Post).get(post_id)
        if post:
            if title: post.title = title
            if content: post.content = content
            try:
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error updating post: {e}")
                return False
        return False

def delete_user(user_id):
    with Session() as session:
        user = session.query(User).get(user_id)
        if user:
            try:
                session.delete(user)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error deleting user: {e}")
                return False
        return False

def delete_post(post_id):
    with Session() as session:
        post = session.query(Post).get(post_id)
        if post:
            try:
                session.delete(post)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Error deleting post: {e}")
                return False
        return False
