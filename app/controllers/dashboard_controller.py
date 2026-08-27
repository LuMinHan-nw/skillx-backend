from sqlalchemy.orm import Session

from app.services import dashboard_service
from app.utils.response import success_response


def summary(db: Session):
    return success_response("Dashboard summary", dashboard_service.summary(db))


def top_skills(db: Session):
    return success_response(
        "Top requested skills", dashboard_service.top_skills(db)
    )


def top_students(db: Session):
    return success_response(
        "Top rated students", dashboard_service.top_students(db)
    )


def exchanges_weekly(db: Session):
    return success_response(
        "Completed exchanges per week", dashboard_service.exchanges_weekly(db)
    )


def rating_by_category(db: Session):
    return success_response(
        "Average rating per category", dashboard_service.rating_by_category(db)
    )
