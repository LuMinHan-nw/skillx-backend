from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skill_id: int
    file_name: str
    uploaded_at: datetime
