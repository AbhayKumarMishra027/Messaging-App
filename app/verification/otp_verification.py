from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base


class OTPPurpose(enum.Enum):
    SIGNUP = "SIGNUP"
    LOGIN = "LOGIN"
    RESET_PASSWORD = "RESET_PASSWORD"
    CHANGE_EMAIL = "CHANGE_EMAIL"

class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # optional during signup
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)

    # needed before user exists
    email = Column(String, nullable=False, index=True)

    otp_hash = Column(String, nullable=False)

    purpose = Column(Enum(OTPPurpose), nullable=False)

    otp_expiry = Column(DateTime(timezone=True), nullable=False)

    is_used = Column(Boolean, default=False)

    attempt_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")