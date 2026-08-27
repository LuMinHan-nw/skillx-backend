import secrets
from datetime import datetime

from fpdf import FPDF
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.certificate import Certificate
from app.models.skill import Skill


def issue(db: Session, student_id: int, sessions_completed: int) -> Certificate:
    certificate = Certificate(
        student_id=student_id,
        certificate_code=f"CERT-{datetime.now().year}-{secrets.token_hex(3).upper()}",
        sessions_completed=sessions_completed,
    )
    db.add(certificate)
    return certificate


def list_mine(db: Session, student_id: int):
    return (
        db.query(Certificate)
        .filter(Certificate.student_id == student_id)
        .order_by(Certificate.issued_at.desc())
        .all()
    )


def get_certificate(db: Session, certificate_id: int) -> Certificate | None:
    return db.query(Certificate).filter(Certificate.id == certificate_id).first()


def list_all(db: Session):
    return db.query(Certificate).order_by(Certificate.issued_at.desc()).all()


def list_for_tutor(db: Session, tutor_id: int):
    learner_ids = (
        db.query(Booking.learner_id)
        .join(Skill, Booking.skill_id == Skill.id)
        .filter(Skill.tutor_id == tutor_id)
        .distinct()
    )
    return (
        db.query(Certificate)
        .filter(Certificate.student_id.in_(learner_ids))
        .order_by(Certificate.issued_at.desc())
        .all()
    )


def delete(db: Session, certificate_id: int) -> bool:
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        return False
    db.delete(certificate)
    db.commit()
    return True


def find_by_code(db: Session, code: str) -> Certificate | None:
    return (
        db.query(Certificate)
        .filter(Certificate.certificate_code == code)
        .first()
    )


def generate_pdf(certificate: Certificate) -> bytes:
    pdf = FPDF(orientation="L", format="A4")
    pdf.add_page()
    pdf.set_draw_color(14, 124, 102)
    pdf.set_line_width(1.5)
    pdf.rect(8, 8, 281, 194)

    pdf.set_y(45)
    pdf.set_font("Helvetica", "B", 34)
    pdf.set_text_color(22, 50, 79)
    pdf.cell(0, 16, "Certificate of Completion", align="C")

    pdf.set_y(75)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(51, 65, 78)
    pdf.cell(0, 10, "SkillX - Student Skill Exchange Platform", align="C")

    pdf.set_y(100)
    pdf.set_font("Helvetica", "", 13)
    pdf.cell(0, 8, "This certificate is proudly presented to", align="C")

    pdf.set_y(115)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(14, 124, 102)
    pdf.cell(0, 14, certificate.student.name, align="C")

    pdf.set_y(138)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(51, 65, 78)
    pdf.cell(
        0, 8,
        f"for successfully completing {certificate.sessions_completed} "
        "peer learning sessions",
        align="C",
    )

    pdf.set_y(165)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(122, 135, 148)
    issued = certificate.issued_at.strftime("%d %B %Y")
    pdf.cell(
        0, 6,
        f"Certificate code: {certificate.certificate_code}   |   Issued: {issued}",
        align="C",
    )
    return bytes(pdf.output())
