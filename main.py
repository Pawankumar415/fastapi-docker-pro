from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import Base, engine, get_db

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def welcome():
    return {"message": "Welcome! FastAPI + MySQL connection working 🎉"}

@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    new_user = User(name=name, email=email)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
