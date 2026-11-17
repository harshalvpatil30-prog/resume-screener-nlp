import spacy
from spacy.matcher import PhraseMatcher
from extract import split_sections

def weighted_skills(text: str) -> dict:
    """Return {skill: weight}. Skills shown in projects/experience count more."""
    sections = split_sections(text)
    weights = {"skills": 1.0, "summary": 1.0,
               "projects": 1.5, "experience": 2.0}
    found = {}
    for name, body in sections.items():
        w = weights.get(name, 0.5)
        for s in extract_skills(body):
            found[s] = max(found.get(s, 0), w)
    return found

nlp = spacy.load("en_core_web_sm")

def build_matcher(skill_file="skills_list.txt"):
    skills = [s.strip().lower() for s in open(skill_file) if s.strip()]
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("SKILL", [nlp.make_doc(s) for s in skills])
    return matcher

MATCHER = build_matcher()

ALIASES = {
    "natural language processing": "nlp",
    "llms": "llm",
    "rest apis": "rest api",
}

def extract_skills(text: str) -> set:
    doc = nlp(text)
    found = {doc[s:e].text.lower() for _, s, e in MATCHER(doc)}
    return {ALIASES.get(s, s) for s in found}      # map synonyms to one canonical name

PROOF_SECTIONS = {"experience", "projects"}   # skills shown in real work
LISTED_CREDIT = 0.6                           # skills only listed or claimed

def skill_credits(text: str) -> dict:
    """Return {skill: credit}. 1.0 if used in experience/projects, else 0.6."""
    sections = split_sections(text)
    if set(sections) == {"other"}:            # no headings found, so we can't tell
        return {s: 1.0 for s in extract_skills(text)}
    credits = {}
    for name, body in sections.items():
        c = 1.0 if name in PROOF_SECTIONS else LISTED_CREDIT
        for s in extract_skills(body):
            credits[s] = max(credits.get(s, 0), c)   # keep the best evidence
    return credits