import mimetypes

from fastapi import HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.material_schema import MaterialResponse
from app.services import material_service, skill_service
from app.utils.response import success_response


def list_materials(skill_id: int, db: Session, current_user: User):
    skill = skill_service.get_skill(db, skill_id)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )
    if not material_service.can_access(db, skill, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Book this skill to see its learning materials",
        )
    materials = material_service.list_for_skill(db, skill.id)
    return success_response(
        "Learning materials",
        [MaterialResponse.model_validate(m).model_dump() for m in materials],
    )


async def upload_material(
    skill_id: int, file: UploadFile, db: Session, current_user: User
):
    skill = skill_service.get_skill(db, skill_id)
    if skill is None or skill.tutor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload materials for your own skills",
        )

    content = await file.read()
    result = material_service.upload(db, skill, file.filename or "material", content)
    if isinstance(result, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
    return success_response(
        "Learning material uploaded",
        MaterialResponse.model_validate(result).model_dump(),
    )


def delete_material(skill_id: int, material_id: int, db: Session, current_user: User):
    skill = skill_service.get_skill(db, skill_id)
    if skill is None or skill.tutor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage materials for your own skills",
        )
    material = material_service.get_material(db, material_id)
    if material is None or material.skill_id != skill.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Material not found"
        )
    material_service.delete(db, material)
    return success_response("Learning material removed")


def download_material(material_id: int, db: Session, current_user: User):
    material = material_service.get_material(db, material_id)
    if material is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Material not found"
        )
    skill = skill_service.get_skill(db, material.skill_id)
    if skill is None or not material_service.can_access(db, skill, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Book this skill to download its learning materials",
        )

    content = material_service.read_file(material)
    media_type = mimetypes.guess_type(material.file_name)[0] or "application/octet-stream"
    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{material.file_name}"'
        },
    )
