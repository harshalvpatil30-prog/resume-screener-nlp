import sys
sys.path.append("src")

from pipeline import rank_candidates

jd = open("data/jobs/job1.txt", encoding="utf-8").read()
required = {"python", "sql", "machine learning", "nlp", "pandas", "git"}
preferred = {"docker", "aws", "pytorch", "hugging face", "fastapi"}

weighted = len(sys.argv) > 1 and sys.argv[1] == "weighted"
result = rank_candidates("data/resumes", jd, required, preferred, weighted=weighted)
print(result[["candidate", "score", "semantic", "required_hit", "missing"]].to_string())
result.to_csv("ranking.csv", index=False)
print("\nSaved to ranking.csv")