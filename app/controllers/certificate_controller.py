from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.certificate_schema import CertificateResponse
from app.services import certificate_service
from app.utils.response import success_response


def list_mine(db: Session, current_user: User):
    certificates = certificate_service.list_mine(db, current_user.id)
    return success_response(
        "My certificates",
        [CertificateResponse.model_validate(c).model_dump() for c in certificates],
    )


def download(certificate_id: int, db: Session, current_user: User):
    certificate = certificate_service.get_certificate(db, certificate_id)
    if certificate is None or certificate.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )

    pdf_bytes = certificate_service.generate_pdf(certificate)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="{certificate.certificate_code}.pdf"'
        },
    )


def list_all(db: Session):
    certificates = certificate_service.list_all(db)
    data = []
    for c in certificates:
        item = CertificateResponse.model_validate(c).model_dump()
        item["student"] = c.student.name if c.student else None
        data.append(item)
    return success_response("All certificates", data)


def list_for_my_learners(db: Session, current_user: User):
    certificates = certificate_service.list_for_tutor(db, current_user.id)
    data = []
    for c in certificates:
        item = CertificateResponse.model_validate(c).model_dump()
        item["student"] = c.student.name if c.student else None
        data.append(item)
    return success_response("Certificates earned by your learners", data)


def remove(certificate_id: int, db: Session):
    if not certificate_service.delete(db, certificate_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    return success_response("Certificate removed")


def verify(code: str, db: Session):
    certificate = certificate_service.find_by_code(db, code)
    if certificate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate code not found",
        )
    return success_response(
        "Certificate is valid",
        {
            "certificate_code": certificate.certificate_code,
            "student": certificate.student.name,
            "sessions_completed": certificate.sessions_completed,
            "issued_at": str(certificate.issued_at),
        },
    )
