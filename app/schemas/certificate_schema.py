from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    certificate_code: str
    sessions_completed: int
    issued_at: datetime
