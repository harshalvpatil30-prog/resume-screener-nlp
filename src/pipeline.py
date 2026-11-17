import pandas as pd
from pathlib import Path
from extract import read_resume
from skills import extract_skills, skill_credits
from scorer import chunked_score, skill_overlap, weighted_overlap, final_score

SUPPORTED = {".pdf", ".docx"}

def rank_candidates(resume_dir, jd_text, required, preferred, weighted=False):
    rows = []
    for f in sorted(Path(resume_dir).glob("*")):
        if f.suffix.lower() not in SUPPORTED:
            continue
        try:
            text = read_resume(f)
        except Exception as e:
            print(f"Skipping {f.name}: {e}")
            continue

        sem = chunked_score(text, jd_text)
        if weighted:
            credits = skill_credits(text)
            skills = set(credits)
            req, pref = weighted_overlap(credits, required, preferred)
        else:
            skills = extract_skills(text)
            req, pref = skill_overlap(skills, required, preferred)

        rows.append({
            "candidate": f.stem,
            "score": final_score(sem, req, pref),
            "semantic": round(sem, 3),
            "required_hit": round(req, 2),
            "preferred_hit": round(pref, 2),
            "matched": ", ".join(sorted(skills & required)),
            "missing": ", ".join(sorted(required - skills)),
        })

    df = pd.DataFrame(rows).sort_values("score", ascending=False)
    return df.reset_index(drop=True)