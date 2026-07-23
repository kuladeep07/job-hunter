from beanie import Document


class Shortlists(Document):
    link: str
    title: str
    portal: str
    match_percent: float

    class Settings:
        name = "shortlists"