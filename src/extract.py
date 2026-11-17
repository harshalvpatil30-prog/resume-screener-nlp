import pdfplumber, docx, re
from pathlib import Path

def read_resume(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        with pdfplumber.open(p) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif p.suffix.lower() == ".docx":
        text = "\n".join(par.text for par in docx.Document(p).paragraphs)
    else:
        raise ValueError("Unsupported file type")
    return clean(text)

def clean(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"-\n(\w)", r"\1", text)
    return text.strip()

SECTION_KEYWORDS = {
    "skills": ["skills", "technologies", "tech stack", "tools"],
    "experience": ["experience", "internship", "employment", "work history", "training"],
    "education": ["education", "academic"],
    "projects": ["projects"],
    "certifications": ["certification", "courses", "achievements"],
    "summary": ["summary", "objective", "profile", "about"],
}

def detect_header(line: str):
    key = line.strip().lower().rstrip(":")
    if not key or len(key.split()) > 4:      # headings are short
        return None
    for section, words in SECTION_KEYWORDS.items():
        if any(w in key for w in words):
            return section
    return None

def split_sections(text: str) -> dict:
    sections, current = {"other": []}, "other"
    for line in text.split("\n"):
        header = detect_header(line)
        if header:
            current = header
            sections.setdefault(current, [])
        else:
            sections[current].append(line)
    return {k: "\n".join(v) for k, v in sections.items()}