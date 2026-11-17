import sys
sys.path.append("src")

from extract import read_resume
from skills import extract_skills
from scorer import chunked_score, skill_overlap, final_score

resume = read_resume("data/resumes/Resume_XYZ_formula.pdf")   # change the name
jd = open("data/jobs/job1.txt", encoding="utf-8").read()

required = {"python", "sql", "machine learning", "nlp", "pandas", "git"}
preferred = {"docker", "aws", "pytorch", "hugging face", "fastapi"}

skills = extract_skills(resume)
sem = chunked_score(resume, jd)
req, pref = skill_overlap(skills, required, preferred)

print("Semantic similarity:", round(sem, 3))
print("Required hit rate:  ", round(req, 2))
print("Preferred hit rate: ", round(pref, 2))
print("Matched required:   ", sorted(skills & required))
print("Missing required:   ", sorted(required - skills))
print("FINAL SCORE:        ", final_score(sem, req, pref))