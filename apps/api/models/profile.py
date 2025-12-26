from pydantic import BaseModel
from typing import List, Optional

class ExperienceItem(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    location: Optional[str] = None
    bullets: List[str] = []

class Profile(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

    summary: Optional[str] = None
    skills: List[str] = []
    technologies: List[str] = []

    experiences: List[ExperienceItem] = []
