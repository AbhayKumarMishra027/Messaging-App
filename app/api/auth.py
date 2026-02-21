from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
import random
import hashlib
from datetime import datetime, timedelta, timezone
from app.models import OTPVerification, OTPPurpose


router = APIRouter()


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup/request-otp")
def request_otp(email: str, db: Session = Depends(get_db)):

    # 1️⃣ Generate 6 digit OTP
    otp = str(random.randint(100000, 999999))

    # 2️⃣ Hash it
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()

    # 3️⃣ Expiry (5 minutes)
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=5)

    # 4️⃣ Create DB entry
    otp_entry = OTPVerification(
        email=email,
        otp_hash=otp_hash,
        purpose=OTPPurpose.SIGNUP,
        otp_expiry=expiry_time,
        is_used=False,
        attempt_count=0
    )

    db.add(otp_entry)
    db.commit()
    db.refresh(otp_entry)

    print(f"Generated OTP for {email}: {otp}")

    return {"message": "OTP generated (check server logs)"}


@router.post("/signup/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):

    # 1️⃣ Fetch latest unused OTP for this email
    otp_entry = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.email == email,
            OTPVerification.is_used == False
        )
        .order_by(OTPVerification.created_at.desc())
        .first()
    )

    if not otp_entry:
        return {"error": "No OTP found for this email"}

    # 2️⃣ Expiry check
    if datetime.now(timezone.utc) > otp_entry.otp_expiry:
    	otp_entry.is_used = True
    	db.commit()
    	return {"error": "OTP expired"}

    # 3️⃣ Attempt limit check
    if otp_entry.attempt_count >= 5:
        return {"error": "Too many attempts. Request new OTP"}

    # 4️⃣ Hash match
    entered_hash = hashlib.sha256(otp.encode()).hexdigest()

    if entered_hash != otp_entry.otp_hash:
        otp_entry.attempt_count += 1
        db.commit()
        return {"error": "Invalid OTP"}

    # 5️⃣ Mark as used
    otp_entry.is_used = True
    db.commit()

    return {"message": "OTP verified successfully ✅"}