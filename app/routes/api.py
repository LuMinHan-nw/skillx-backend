from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.controllers import (
    admin_controller,
    auth_controller,
    booking_controller,
    certificate_controller,
    complaint_controller,
    dashboard_controller,
    feedback_controller,
    material_controller,
    notification_controller,
    password_reset_controller,
    skill_controller,
    user_controller,
)
from app.database import get_db
from app.middleware.auth_middleware import get_current_user, require_roles
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.schemas.booking_schema import (
    BookingCancel,
    BookingCreate,
    BookingMeetingLink,
    BookingReschedule,
)
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.schemas.complaint_schema import ComplaintCreate, ComplaintResolve
from app.schemas.feedback_schema import FeedbackCreate, FeedbackUpdate
from app.schemas.password_reset_schema import (
    PasswordResetComplete,
    PasswordResetRequestCreate,
)
from app.schemas.skill_schema import AvailabilityCreate, SkillCreate, SkillUpdate
from app.schemas.user_schema import UserUpdate

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/auth/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_controller.register(data, db)


@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_controller.login(data, db)


@router.get("/auth/me")
def me(current_user: User = Depends(get_current_user)):
    return auth_controller.me(current_user)


@router.put("/users/me")
def update_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_controller.update_profile(data, db, current_user)


@router.post("/users/me/picture")
async def upload_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_controller.upload_picture(file, db, current_user)


@router.get("/users/{user_id}/profile")
def public_profile(user_id: int, db: Session = Depends(get_db)):
    return user_controller.public_profile(user_id, db)


@router.get("/skills")
def list_skills(
    category_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return skill_controller.list_skills(db, category_id, search)


@router.get("/skills/categories")
def list_categories(db: Session = Depends(get_db)):
    return skill_controller.list_categories(db)


@router.get("/skills/mine")
def list_my_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return skill_controller.list_my_skills(db, current_user)


@router.get("/skills/{skill_id}")
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return skill_controller.get_skill(skill_id, db, current_user)


@router.post("/skills")
def create_skill(
    data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return skill_controller.create_skill(data, db, current_user)


@router.put("/skills/{skill_id}")
def update_skill(
    skill_id: int,
    data: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return skill_controller.update_skill(skill_id, data, db, current_user)


@router.delete("/skills/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return skill_controller.delete_skill(skill_id, db, current_user)


@router.post("/skills/{skill_id}/availability")
def add_availability(
    skill_id: int,
    data: AvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return skill_controller.add_availability(skill_id, data, db, current_user)


@router.delete("/skills/{skill_id}/availability/{slot_id}")
def delete_availability(
    skill_id: int,
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return skill_controller.delete_availability(skill_id, slot_id, db, current_user)


@router.get("/skills/{skill_id}/materials")
def list_materials(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return material_controller.list_materials(skill_id, db, current_user)


@router.post("/skills/{skill_id}/materials")
async def upload_material(
    skill_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return await material_controller.upload_material(skill_id, file, db, current_user)


@router.delete("/skills/{skill_id}/materials/{material_id}")
def delete_material(
    skill_id: int,
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return material_controller.delete_material(skill_id, material_id, db, current_user)


@router.get("/materials/{material_id}/download")
def download_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return material_controller.download_material(material_id, db, current_user)


@router.post("/bookings")
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.create_booking(data, db, current_user)


@router.get("/bookings/mine")
def list_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.list_my_bookings(db, current_user)


@router.put("/bookings/{booking_id}/accept")
def accept_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.accept(booking_id, db, current_user)


@router.put("/bookings/{booking_id}/decline")
def decline_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.decline(booking_id, db, current_user)


@router.put("/bookings/{booking_id}/complete")
def complete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.complete(booking_id, db, current_user)


@router.put("/bookings/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    data: BookingCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.cancel(booking_id, data, db, current_user)


@router.put("/bookings/{booking_id}/reschedule")
def reschedule_booking(
    booking_id: int,
    data: BookingReschedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.reschedule(booking_id, data, db, current_user)


@router.put("/bookings/{booking_id}/meeting-link")
def set_booking_meeting_link(
    booking_id: int,
    data: BookingMeetingLink,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return booking_controller.set_meeting_link(booking_id, data, db, current_user)


@router.post("/feedback")
def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return feedback_controller.submit(data, db, current_user)


@router.get("/feedback/pending")
def pending_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return feedback_controller.pending(db, current_user)


@router.put("/feedback/{feedback_id}")
def update_feedback(
    feedback_id: int,
    data: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return feedback_controller.update(feedback_id, data, db, current_user)


@router.post("/complaints")
def submit_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return complaint_controller.submit(data, db, current_user)


@router.get("/complaints/mine")
def list_my_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return complaint_controller.list_mine(db, current_user)


@router.get("/certificates/mine")
def my_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return certificate_controller.list_mine(db, current_user)


@router.get("/certificates/verify/{code}")
def verify_certificate(code: str, db: Session = Depends(get_db)):
    return certificate_controller.verify(code, db)


@router.get("/certificates/my-learners")
def my_learners_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return certificate_controller.list_for_my_learners(db, current_user)


@router.get("/certificates/{certificate_id}/download")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("student")),
):
    return certificate_controller.download(certificate_id, db, current_user)


@router.get("/notifications")
def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_controller.list_notifications(db, current_user)


@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_controller.mark_read(notification_id, db, current_user)


@router.get("/admin/skills/pending")
def admin_pending_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.pending_skills(db)


@router.put("/admin/skills/{skill_id}/approve")
def admin_approve_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.review_skill(skill_id, True, db, current_user)


@router.put("/admin/skills/{skill_id}/reject")
def admin_reject_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.review_skill(skill_id, False, db, current_user)


@router.get("/admin/users")
def admin_list_users(
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.list_users(db, search)


@router.put("/admin/users/{user_id}/suspend")
def admin_suspend_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.set_user_status(user_id, "suspended", db)


@router.put("/admin/users/{user_id}/reactivate")
def admin_reactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.set_user_status(user_id, "active", db)


@router.put("/admin/users/{user_id}")
def admin_update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.update_user_info(user_id, data, db)


@router.get("/admin/certificates")
def admin_list_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return certificate_controller.list_all(db)


@router.delete("/admin/certificates/{certificate_id}")
def admin_delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return certificate_controller.remove(certificate_id, db)


@router.post("/auth/password-reset/request")
def request_password_reset(
    data: PasswordResetRequestCreate, db: Session = Depends(get_db)
):
    return password_reset_controller.request_reset(data, db)


@router.post("/auth/password-reset/complete")
def complete_password_reset(
    data: PasswordResetComplete, db: Session = Depends(get_db)
):
    return password_reset_controller.complete_reset(data, db)


@router.get("/admin/password-resets")
def admin_list_password_resets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return password_reset_controller.list_all(db)


@router.put("/admin/password-resets/{request_id}/approve")
def admin_approve_password_reset(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return password_reset_controller.approve(request_id, db)


@router.get("/admin/complaints")
def admin_list_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return complaint_controller.list_all(db)


@router.put("/admin/complaints/{complaint_id}/resolve")
def admin_resolve_complaint(
    complaint_id: int,
    data: ComplaintResolve,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return complaint_controller.resolve(complaint_id, data, db)


@router.get("/admin/feedback")
def admin_list_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.list_feedback(db)


@router.post("/admin/categories")
def admin_create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.create_category(data, db)


@router.put("/admin/categories/{category_id}")
def admin_update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.update_category(category_id, data, db)


@router.delete("/admin/categories/{category_id}")
def admin_delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return admin_controller.delete_category(category_id, db)


@router.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return dashboard_controller.summary(db)


@router.get("/dashboard/top-skills")
def dashboard_top_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return dashboard_controller.top_skills(db)


@router.get("/dashboard/top-students")
def dashboard_top_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return dashboard_controller.top_students(db)


@router.get("/dashboard/exchanges-weekly")
def dashboard_exchanges_weekly(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return dashboard_controller.exchanges_weekly(db)


@router.get("/dashboard/rating-by-category")
def dashboard_rating_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
):
    return dashboard_controller.rating_by_category(db)
