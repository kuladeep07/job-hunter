from datetime import datetime

from beanie import Document


class ProcessedJobs(Document):
    link: str
    portal: str
    match_percent: float
    processed_at: datetime

    class Settings:
        name = "processed_jobs"
