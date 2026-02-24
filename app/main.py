from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from app import schemas, database
from app import models
from uuid import UUID


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
    
@app.post("/messages/", response_model=schemas.MessageResponse)
def send_message(message: schemas.MessageCreate, sender_id: UUID, db: Session = Depends(get_db)):
    conversation = db.query(models.Conversation).filter(
        or_(
            (models.Conversation.user1_id == sender_id) & (models.Conversation.user2_id == message.receiver_id),
            (models.Conversation.user1_id == message.receiver_id) & (models.Conversation.user2_id == sender_id)
        )
    ).first()

    if not conversation:
        conversation = models.Conversation(
            user1_id=sender_id,
            user2_id=message.receiver_id
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    new_message = models.Message(
        conversation_id=conversation.id,
        sender_id=sender_id,
        content=message.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

