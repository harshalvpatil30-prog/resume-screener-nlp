"""
Estimates screening-time reduction.
- Tool runtime is MEASURED (includes model loading, so it is conservative).
- Manual time per resume is an ASSUMPTION taken from published research.
Run from project root:  python estimate_time_saved.py
"""
import sys, time
t0 = time.perf_counter()                 # start BEFORE imports so model loading is counted
sys.path.append("src")
from pipeline import rank_candidates

jd = open("data/jobs/job1.txt", encoding="utf-8").read()
required = {"python", "sql", "machine learning", "nlp", "pandas", "git"}
preferred = {"docker", "aws", "pytorch", "hugging face", "fastapi"}

result = rank_candidates("data/resumes", jd, required, preferred, weighted=True)
tool_minutes = (time.perf_counter() - t0) / 60
n = len(result)
print(f"Resumes processed: {n}")
print(f"MEASURED tool runtime (incl. model load): {tool_minutes * 60:.1f} seconds\n")

# ---- Assumptions (state these in your README) ----
# Recruiters self-reported 4-5 min per resume (TheLadders, 2012 eye-tracking study).
# After the tool, a human still reads the shortlist, so that time is counted too.
print(f"{'Manual min/resume':>18}{'Shortlist reviewed':>20}{'Manual (min)':>14}{'Tool (min)':>12}{'Reduction':>11}")
for manual_per in (3, 4, 5):
    for shortlist in (5, 10):
        manual = n * manual_per
        tool = tool_minutes + shortlist * manual_per      # human reviews the shortlist at same pace
        reduction = (manual - tool) / manual * 100
        print(f"{manual_per:>18}{shortlist:>20}{manual:>14.0f}{tool:>12.1f}{reduction:>10.0f}%")
