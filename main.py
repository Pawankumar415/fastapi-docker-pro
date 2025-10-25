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


@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields only if they are provided
    if name:
        user.name = name
    if email:
        user.email = email

    try:
        db.commit()
        db.refresh(user)
        return {
            "message": "User updated successfully",
            "user": {"id": user.id, "name": user.name, "email": user.email}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
