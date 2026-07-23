from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumesRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_name: str
    skills: list[str]
    uploaded_at: datetime
