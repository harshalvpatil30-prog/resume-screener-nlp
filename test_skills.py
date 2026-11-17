import sys
sys.path.append("src")

from extract import read_resume
from skills import extract_skills

text = read_resume("data/resumes/Resume_XYZ_formula.pdf")
print(extract_skills(text))