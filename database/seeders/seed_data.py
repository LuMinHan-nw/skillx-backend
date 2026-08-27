import sys
from datetime import date, time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from app.database import SessionLocal
from app.models.booking import Booking
from app.models.complaint import Complaint
from app.models.feedback import Feedback
from app.models.notification import Notification
from app.models.skill import Skill, SkillCategory, TutorAvailability
from app.models.user import User
from app.services.material_service import STORAGE_DIR
from app.models.material import SkillMaterial
from app.utils.password_handler import hash_password


def get_or_create_user(db, name, email, password, role, bio=None):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user

    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role=role,
        bio=bio,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_category(db, name, description):
    category = db.query(SkillCategory).filter(SkillCategory.name == name).first()
    if category:
        return category

    category = SkillCategory(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_or_create_skill(db, tutor_id, category_id, name, description, proficiency,
                        status, approved_by=None, duration=60):
    skill = db.query(Skill).filter(Skill.name == name).first()
    if skill:
        return skill

    skill = Skill(
        tutor_id=tutor_id,
        category_id=category_id,
        approved_by=approved_by,
        name=name,
        description=description,
        proficiency=proficiency,
        status=status,
        session_duration_minutes=duration,
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def seed():
    db = SessionLocal()
    try:
        admin = get_or_create_user(
            db, "Zaw Myo Htet", "admin@skillx-demo.com", "admin123", "admin"
        )
        aung = get_or_create_user(
            db, "Aung Kyaw Min", "aungkyaw@skillx-demo.com", "student123", "student",
            "Computer Science major interested in Web Development.",
        )
        thiri = get_or_create_user(
            db, "Thiri San", "thirisan@skillx-demo.com", "student123", "student",
            "UX/UI Design student who loves building interfaces.",
        )
        hsu = get_or_create_user(
            db, "Hsu Myat Noe", "hsumyat@skillx-demo.com", "student123", "student",
            "Data Science enthusiast passionate about ML.",
        )

        web = get_or_create_category(
            db, "Web Development", "Frontend and backend web technologies."
        )
        data = get_or_create_category(
            db, "Data Science", "Data analysis, statistics and machine learning."
        )
        design = get_or_create_category(
            db, "Design & UX", "UI/UX design, wireframing and design tools."
        )
        get_or_create_category(
            db, "Languages", "Spoken and written language practice."
        )
        get_or_create_category(
            db, "Soft Skills", "Communication, presentation and teamwork."
        )

        react = get_or_create_skill(
            db, aung.id, web.id, "ReactJS Development",
            "Modern single-page apps with hooks and context.",
            "advanced", "approved", admin.id, 90,
        )
        figma = get_or_create_skill(
            db, thiri.id, design.id, "Figma Wireframing",
            "High-fidelity prototypes and UI component libraries.",
            "intermediate", "approved", admin.id,
        )
        get_or_create_skill(
            db, hsu.id, data.id, "Python Data Analysis with Pandas",
            "EDA, data cleaning and visualisation.",
            "intermediate", "pending",
        )

        if not db.query(TutorAvailability).first():
            db.add_all([
                TutorAvailability(skill_id=react.id, day_of_week=2,
                                  start_time=time(14, 0), end_time=time(17, 0)),
                TutorAvailability(skill_id=react.id, day_of_week=6,
                                  start_time=time(10, 0), end_time=time(12, 0)),
                TutorAvailability(skill_id=figma.id, day_of_week=4,
                                  start_time=time(9, 0), end_time=time(11, 0)),
            ])
            db.commit()

        if not db.query(Booking).first():
            completed = Booking(
                skill_id=react.id, learner_id=thiri.id,
                session_date=date(2026, 7, 1),
                start_time=time(13, 0), end_time=time(15, 0),
                status="completed",
            )
            pending = Booking(
                skill_id=figma.id, learner_id=hsu.id,
                session_date=date(2026, 7, 18),
                start_time=time(9, 30), end_time=time(11, 0),
                status="pending",
            )
            db.add_all([completed, pending])
            db.commit()
            db.refresh(completed)

            db.add(Feedback(
                booking_id=completed.id, given_by=thiri.id, given_to=aung.id,
                rating=5,
                comments="Explained React state perfectly. Recommended!",
            ))
            db.add(Notification(
                user_id=aung.id,
                message="Your skill 'ReactJS Development' was approved.",
            ))
            db.add(Notification(
                user_id=thiri.id,
                message="Reminder: your ReactJS session is coming up.",
            ))
            db.commit()

            # Thiri is one completed session away from her first certificate
            # (CERTIFICATE_SESSION_TARGET=5). These 3 plus the one above put
            # her at 4 completed sessions as a learner, so booking and
            # completing one more ReactJS session live will trigger it.
            db.add_all([
                Booking(
                    skill_id=react.id, learner_id=thiri.id,
                    session_date=date(2026, 7, 8),
                    start_time=time(14, 0), end_time=time(15, 30),
                    status="completed",
                ),
                Booking(
                    skill_id=react.id, learner_id=thiri.id,
                    session_date=date(2026, 7, 15),
                    start_time=time(14, 0), end_time=time(15, 30),
                    status="completed",
                ),
                Booking(
                    skill_id=react.id, learner_id=thiri.id,
                    session_date=date(2026, 7, 22),
                    start_time=time(14, 0), end_time=time(15, 30),
                    status="completed",
                ),
            ])
            db.commit()

        if not db.query(SkillMaterial).first():
            STORAGE_DIR.mkdir(parents=True, exist_ok=True)
            stored_name = "skill1_seed_notes.md"
            (STORAGE_DIR / stored_name).write_text(
                "# React Hooks Cheat Sheet\n\n"
                "useState, useEffect, useContext - quick reference and examples.\n",
                encoding="utf-8",
            )
            db.add(SkillMaterial(
                skill_id=react.id,
                file_name="react-hooks-cheatsheet.md",
                stored_path=stored_name,
            ))
            db.commit()

        if not db.query(Complaint).first():
            db.add(Complaint(
                submitted_by=hsu.id,
                subject="Session materials never shared",
                message="My tutor said they would send prep notes before the "
                        "session but I never received anything.",
            ))
            db.commit()

        print("Seed data inserted successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
