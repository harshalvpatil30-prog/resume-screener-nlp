from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_score(resume_text: str, jd_text: str) -> float:
    emb = model.encode([resume_text, jd_text], convert_to_tensor=True)
    return float(util.cos_sim(emb[0], emb[1]))

def chunked_score(resume_text, jd_text, chunk_size=200):
    words = resume_text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    sims = util.cos_sim(model.encode(chunks, convert_to_tensor=True), jd_emb)
    return float(sims.max())

def skill_overlap(resume_skills: set, required: set, preferred: set):
    req_hit = len(resume_skills & required) / max(len(required), 1)
    pref_hit = len(resume_skills & preferred) / max(len(preferred), 1)
    return req_hit, pref_hit

def weighted_overlap(credits: dict, required: set, preferred: set):
    req_hit = sum(credits.get(s, 0) for s in required) / max(len(required), 1)
    pref_hit = sum(credits.get(s, 0) for s in preferred) / max(len(preferred), 1)
    return req_hit, pref_hit

def final_score(sem, req_hit, pref_hit):
    return round(100 * (0.40 * req_hit + 0.15 * pref_hit + 0.45 * sem), 1)

