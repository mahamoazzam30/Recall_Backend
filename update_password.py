"""
Script to update demo.recall@gmail.com password to demopass123
Run with: python update_password.py
"""
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import hash_password


def update_demo_password():
    db: Session = SessionLocal()
    try:
        # Hash the new password
        new_hashed_password = hash_password("demopass123")
        
        # Update the user's password using raw SQL to avoid relationship issues
        result = db.execute(
            text("UPDATE users SET hashed_password = :password WHERE email = :email"),
            {"password": new_hashed_password, "email": "demo.recall@gmail.com"}
        )
        
        db.commit()
        
        if result.rowcount > 0:
            print("Password updated successfully for demo.recall@gmail.com")
            print("New password: demopass123")
        else:
            print("User demo.recall@gmail.com not found")
            
    except Exception as e:
        print(f"Error updating password: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    update_demo_password()
