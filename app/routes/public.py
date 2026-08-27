from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.response import success_response


router = APIRouter(tags=["Public"])


@router.get("/health")
def health():
    return success_response("OK")


@router.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return success_response("Database connected successfully")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed",
        )
