import secrets
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.material import SkillMaterial
from app.models.skill import Skill

# Kept outside frontend/ (unlike profile pictures) since materials are only meant
# to be reachable through the authenticated download endpoint, not served as a
# static file to anyone who guesses the URL.
STORAGE_DIR = Path(__file__).resolve().parents[2] / "storage" / "materials"
ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md",
    ".zip", ".png", ".jpg", ".jpeg", ".mp4",
}
MAX_SIZE = 20 * 1024 * 1024


# Two ways to be allowed in: own the listing, or hold a booking on it that is
# still alive. A declined or cancelled booking must not keep granting access,
# which is why those two statuses are excluded rather than checking for a
# confirmed one - a pending request counts too.
def can_access(db: Session, skill: Skill, user) -> bool:
    if skill.tutor_id == user.id:
        return True
    return (
        db.query(Booking)
        .filter(Booking.skill_id == skill.id, Booking.learner_id == user.id)
        .filter(Booking.status.notin_(["declined", "cancelled"]))
        .first()
        is not None
    )


def list_for_skill(db: Session, skill_id: int):
    return (
        db.query(SkillMaterial)
        .filter(SkillMaterial.skill_id == skill_id)
        .order_by(SkillMaterial.uploaded_at.desc())
        .all()
    )


def get_material(db: Session, material_id: int) -> SkillMaterial | None:
    return db.query(SkillMaterial).filter(SkillMaterial.id == material_id).first()


def upload(db: Session, skill: Skill, filename: str, content: bytes) -> SkillMaterial | str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return "That file type isn't allowed"
    if len(content) > MAX_SIZE:
        return "File must be smaller than 20 MB"

    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"skill{skill.id}_{secrets.token_hex(4)}{extension}"
    (STORAGE_DIR / stored_name).write_bytes(content)

    material = SkillMaterial(
        skill_id=skill.id, file_name=filename, stored_path=stored_name,
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def read_file(material: SkillMaterial) -> bytes:
    return (STORAGE_DIR / material.stored_path).read_bytes()


def delete(db: Session, material: SkillMaterial):
    path = STORAGE_DIR / material.stored_path
    if path.exists():
        path.unlink()
    db.delete(material)
    db.commit()
