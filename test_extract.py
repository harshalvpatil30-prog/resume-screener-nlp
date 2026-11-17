import sys
sys.path.append("src")          # lets Python find files inside src/

from extract import read_resume, split_sections

text = read_resume("data/resumes/Resume_XYZ_formula.pdf")   # change the name
print(text[:500])               # first 500 characters
print("-----")
print(split_sections(text).keys())   # which sections were found