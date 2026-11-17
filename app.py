import sys, tempfile
from pathlib import Path
import streamlit as st

sys.path.append("src")
from pipeline import rank_candidates

st.set_page_config(page_title="Resume Screener", layout="wide")
st.title("Candidate Screening & Resume Ranker")

# ---- Inputs ----
jd = st.text_area("Job description", height=200,
                  placeholder="Paste the job description here")

col1, col2 = st.columns(2)
required_txt = col1.text_input("Required skills (comma-separated)",
                               "python, sql, machine learning, nlp, pandas, git")
preferred_txt = col2.text_input("Preferred skills (comma-separated)",
                                "docker, aws, pytorch, hugging face, fastapi")

files = st.file_uploader("Upload resumes (PDF or DOCX)",
                         type=["pdf", "docx"], accept_multiple_files=True)

def to_set(s):
    return {x.strip().lower() for x in s.split(",") if x.strip()}

# ---- Run ----
if st.button("Rank candidates"):
    if not jd.strip() or not files:
        st.warning("Please add a job description and at least one resume.")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            for f in files:
                (Path(tmp) / f.name).write_bytes(f.getbuffer())
            with st.spinner("Analyzing resumes..."):
                result = rank_candidates(tmp, jd, to_set(required_txt), to_set(preferred_txt), weighted=True)

        st.subheader("Ranked candidates")
        st.dataframe(result, use_container_width=True)
        st.download_button("Download CSV", result.to_csv(index=False),
                           "ranking.csv", "text/csv")