from sqlalchemy.orm import Session
from app.models import User


def user_exists(db: Session, email: str, phone_number: str) -> bool:
    """
    Check if user already exists by email OR phone
    """
    return (
        db.query(User)
        .filter((User.email == email) | (User.phone_number == phone_number))
        .first()
        is not None
    )


def create_user(
    db: Session,
    first_name: str,
    last_name: str,
    email: str,
    phone_number: str,
) -> User:
    """
    Create a new inactive user
    """
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        is_active=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user