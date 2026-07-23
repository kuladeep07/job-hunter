from datetime import datetime

from beanie import Document


class Resumes(Document):
    role_name: str
    file_name: str
    raw_text: str
    skills: list[str]
    uploaded_at: datetime


    class Settings:
        name = "resumes"
