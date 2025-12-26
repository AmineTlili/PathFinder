import re
from typing import List
from models.profile import Profile, ExperienceItem

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\s\-\(\)]{7,}\d)")
LOCATION_RE = re.compile(
    r"([A-Za-zÀ-ÖØ-öø-ÿ'\- ]+)\s*(\d{5}),\s*([A-Za-zÀ-ÖØ-öø-ÿ'\- ]+)",
    flags=re.IGNORECASE
)


def _clean_lines(text: str) -> List[str]:
    lines = [l.strip() for l in text.splitlines()]
    lines = [l for l in lines if l]
    return lines

def extract_profile_from_text(text: str) -> Profile:
    lines = _clean_lines(text)

    full_name = lines[0] if lines else None

    email = None
    m = EMAIL_RE.search(text)
    if m:
        email = m.group(0)

    phone = None
    m = PHONE_RE.search(text)
    if m:
        phone = m.group(0).strip()

    location = None
    for l in lines[:15]:  
        m = LOCATION_RE.search(l)
        if m:
            city = m.group(1).strip()
            postal = m.group(2).strip()
            region = m.group(3).strip()
            location = f"{city} {postal}, {region}"
            break

    linkedin = None
    github = None
    for l in lines:
        low = l.lower()
        if "linkedin.com/" in low:
            linkedin = l
        if "github.com/" in low:
            github = l

    headline = lines[1] if len(lines) > 1 else None

    summary = None
    t = text
    prof_match = re.search(r"\bPROFIL\b", t, flags=re.IGNORECASE)
    exp_match = re.search(r"\bEXP[ÉE]RIENCES\b", t, flags=re.IGNORECASE)
    if prof_match and exp_match and exp_match.start() > prof_match.end():
        summary = t[prof_match.end():exp_match.start()].strip()
        summary = re.sub(r"\s+\n", "\n", summary)

    technologies = []
    tech_match = re.findall(r"Technologies?\s*:\s*(.+)", text, flags=re.IGNORECASE)
    for grp in tech_match:
        parts = re.split(r"[,•\|\n]", grp)
        technologies.extend([p.strip() for p in parts if p.strip()])

    seen = set()
    technologies_clean = []
    for x in technologies:
        key = x.lower()
        if key not in seen:
            seen.add(key)
            technologies_clean.append(x)

    profile = Profile(
        full_name=full_name,
        headline=headline,
        email=email,
        phone=phone,
        location=location,
        linkedin=linkedin,
        github=github,
        summary=summary,
        technologies=technologies_clean,
        skills=[],
        experiences=[],
    )
    return profile
