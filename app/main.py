from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import schemas, database
from app import models

app=FastAPI()

def get_db():
    db=database.SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    new_user = models.User(
        phone_number=user.phone_number,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        about=user.about
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError as e: 
        db.rollback()
        print(f"DATABASE ERROR: {e}")
        raise HTTPException(status_code=400, detail=f"Database error")

