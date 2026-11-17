"""
Evaluate the ranker against the human labels.
Run from project root AFTER python test_pipeline.py has created ranking.csv:
    python evaluate.py
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

K = 10
rank = pd.read_csv("ranking.csv")
lab = pd.read_csv("data/labels.csv")
lab["candidate"] = lab["file"].str.replace(r"\.(docx|pdf)$", "", regex=True)

df = rank.merge(lab[["candidate", "label", "note"]], on="candidate")
df["truth"] = df["label"].map({"Good": 2, "Maybe": 1, "Poor": 0})
n_good = int((df["label"] == "Good").sum())


def precision_recall_at_k(frame, k=K):
    top = frame.head(k)
    hits = int((top["label"] == "Good").sum())
    return hits / k, hits / n_good


# ---------- 1. Your tool (hybrid: skills + transformer) ----------
tool = df.sort_values("score", ascending=False).reset_index(drop=True)
p_tool, r_tool = precision_recall_at_k(tool)
rho_tool = spearmanr(tool["score"], tool["truth"]).correlation

# ---------- 2. Keyword-only baseline (no transformer) ----------
# Ties are common here, so break them randomly and average over many runs.
df["kw_score"] = 0.7 * df["required_hit"] + 0.3 * df["preferred_hit"]
rng = np.random.default_rng(0)
ps, rs = [], []
for _ in range(1000):
    shuffled = df.sample(frac=1, random_state=int(rng.integers(1e9)))
    ranked = shuffled.sort_values("kw_score", ascending=False, kind="stable")
    p, r = precision_recall_at_k(ranked)
    ps.append(p)
    rs.append(r)
p_kw, r_kw = float(np.mean(ps)), float(np.mean(rs))
rho_kw = spearmanr(df["kw_score"], df["truth"]).correlation

# ---------- Report ----------
print(f"Resumes: {len(df)}  |  Good: {n_good}\n")
print(f"{'Method':<28}{'Precision@10':>14}{'Recall@10':>12}{'Spearman':>10}")
print(f"{'Keyword-only baseline':<28}{p_kw:>14.2f}{r_kw:>12.2f}{rho_kw:>10.2f}")
print(f"{'Hybrid (skills+transformer)':<28}{p_tool:>14.2f}{r_tool:>12.2f}{rho_tool:>10.2f}")

print("\nWrong candidates in your top 10:")
wrong = tool.head(K)[tool.head(K)["label"] != "Good"]
print(wrong[["candidate", "score", "label", "note"]].to_string(index=False) if len(wrong) else "  none")

print("\nGood candidates ranked outside the top 10 (missed):")
missed = tool.iloc[K:][tool.iloc[K:]["label"] == "Good"]
print(missed[["candidate", "score", "missing", "note"]].to_string(index=False) if len(missed) else "  none")

print("\nPoor candidates with all required skills (keyword traps):")
traps = tool[(tool["label"] == "Poor") & (tool["required_hit"] >= 0.99)]
for i, row in traps.iterrows():
    print(f"  {row['candidate']} ranked #{i + 1} of {len(tool)} (score {row['score']}) - {row['note']}")
