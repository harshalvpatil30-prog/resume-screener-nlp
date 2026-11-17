"""
Generates 30 SYNTHETIC resumes (.docx) + labels.csv (the answer key).
All names, emails and companies are fake. Run from your project root:
    python generate_resumes.py
Output: data/resumes/Candidate_01.docx ... and data/labels.csv
"""
import csv, random
from pathlib import Path
from docx import Document

random.seed(42)
OUT = Path("data/resumes")
OUT.mkdir(parents=True, exist_ok=True)

FIRST = ["Aarav", "Diya", "Rohan", "Sneha", "Kabir", "Meera", "Arjun", "Isha", "Vikram", "Anaya",
         "Nikhil", "Pooja", "Siddharth", "Riya", "Karan", "Tanvi", "Yash", "Neha", "Aditya", "Kavya",
         "Manish", "Shruti", "Rahul", "Pranav", "Sakshi", "Varun", "Ananya", "Harsh", "Divya", "Omkar"]
LAST = ["Sharma", "Patel", "Deshmukh", "Iyer", "Kulkarni", "Reddy", "Joshi", "Nair", "Gupta", "Mehta",
        "Shinde", "Rao", "Verma", "Pawar", "Singh", "Chavan", "Bose", "Jain", "More", "Kapoor"]
CITIES = ["Pune", "Mumbai", "Bengaluru", "Hyderabad", "Nagpur", "Nashik", "Chennai", "Delhi"]

# ---------------------------------------------------------------
# Archetypes: (label, type, title, skills, experience bullets, project bullets, degree)
# ---------------------------------------------------------------
GOOD = [
    ("Strong ML/NLP engineer",
     "Machine Learning Engineer",
     "Python, SQL, Machine Learning, NLP, Pandas, Git, PyTorch, Hugging Face, Docker, FastAPI",
     ["Built and deployed an NLP text classification service using Hugging Face Transformers, serving 5k requests/day.",
      "Fine-tuned BERT models for intent detection and improved F1 score from 0.78 to 0.89.",
      "Wrote SQL and Pandas pipelines to prepare training data; managed code with Git."],
     ["Resume classifier using transformers and scikit-learn.", "REST API with FastAPI, containerised with Docker."],
     "B.Tech in Computer Science"),
    ("ML engineer, cloud focus",
     "AI / ML Engineer",
     "Python, SQL, Machine Learning, Deep Learning, NLP, Pandas, NumPy, Git, AWS, Docker, TensorFlow",
     ["Trained deep learning models for sentiment analysis and deployed them on AWS.",
      "Automated data cleaning using Pandas and SQL, cutting preparation time by 40%.",
      "Collaborated through Git and code reviews in a team of six."],
     ["Customer review sentiment analyzer (NLP).", "Demand forecasting with scikit-learn."],
     "M.Tech in Data Science"),
    ("Good but uses natural language wording",
     "Data Scientist",
     "Python, SQL, Machine Learning, Natural Language Processing, Pandas, Scikit-learn, Git",
     ["Developed models to extract entities from legal documents using natural language processing.",
      "Queried large datasets with SQL and analysed them in Pandas.",
      "Tracked experiments and versioned code with Git."],
     ["Topic modelling on news articles.", "Churn prediction model with scikit-learn."],
     "B.E. in Information Technology"),
    ("Strong fresher, project-heavy",
     "Machine Learning Intern",
     "Python, SQL, Machine Learning, NLP, Pandas, Git, GitHub, PyTorch, Hugging Face",
     ["Intern: built an NLP pipeline to classify support tickets using Hugging Face models.",
      "Cleaned and analysed 200k rows of data using Pandas and SQL."],
     ["Fine-tuned a transformer for question answering.", "Built a Streamlit demo and published code on GitHub."],
     "B.Tech in Electronics and Telecommunication"),
    ("Strong generative AI profile",
     "Generative AI Engineer",
     "Python, SQL, Machine Learning, NLP, LLM, Prompt Engineering, Pandas, Git, Hugging Face, FastAPI",
     ["Built retrieval-augmented generation (RAG) applications using LLMs and FastAPI.",
      "Fine-tuned language models and evaluated outputs with custom metrics.",
      "Maintained data pipelines in Python, Pandas and SQL; used Git for version control."],
     ["Chatbot for HR queries using LLMs.", "Document summarizer using Hugging Face transformers."],
     "B.Tech in Computer Science"),
    ("Experienced ML, few preferred skills",
     "Senior Data Scientist",
     "Python, SQL, Machine Learning, NLP, Pandas, NumPy, Git, Scikit-learn",
     ["Led a team of four building recommendation and text-mining models over 3 years.",
      "Designed NLP features that lifted conversion by 12%.",
      "Mentored juniors on Python, SQL and Git workflows."],
     ["Fraud detection model.", "Customer segmentation with clustering."],
     "M.Sc. in Statistics"),
    ("Good, wording differs (ML as 'AI')",
     "AI Developer",
     "Python, SQL, Pandas, Git, Machine Learning, NLP, PyTorch, Docker",
     ["Developed AI features for a SaaS product including text classification and keyword extraction.",
      "Built data processing scripts in Python and SQL.",
      "Containerised models using Docker and deployed via CI."],
     ["Spam detector using NLP.", "Image classifier in PyTorch."],
     "B.Tech in Computer Science"),
    ("Good MLOps lean",
     "ML Engineer",
     "Python, SQL, Machine Learning, NLP, Pandas, Git, Docker, AWS, Kubernetes, FastAPI",
     ["Productionised NLP models as REST APIs using FastAPI, Docker and Kubernetes.",
      "Monitored model drift and automated retraining on AWS.",
      "Wrote SQL queries and Pandas jobs for feature engineering."],
     ["Search ranking model.", "Model monitoring dashboard."],
     "B.E. in Computer Engineering"),
    ("Good research-flavoured",
     "NLP Research Engineer",
     "Python, SQL, Machine Learning, Deep Learning, NLP, Pandas, Git, PyTorch, Hugging Face",
     ["Researched transformer architectures for low-resource language translation.",
      "Published a paper on text classification; open-sourced the code on GitHub.",
      "Prepared datasets using Pandas and SQL."],
     ["Named entity recognition for Marathi text.", "Evaluation toolkit for language models."],
     "M.Tech in Artificial Intelligence"),
    ("Good, junior with internship",
     "Data Science Intern",
     "Python, SQL, Machine Learning, NLP, Pandas, Git, Scikit-learn, Hugging Face",
     ["Intern: trained text classifiers on customer feedback and presented results to the product team.",
      "Used SQL and Pandas to build analysis datasets."],
     ["Fake news detector using NLP.", "House price prediction with scikit-learn."],
     "B.Sc. in Computer Science"),
]

MAYBE = [
    ("Data analyst: no ML/NLP",
     "Data Analyst",
     "Python, SQL, Pandas, Excel, Power BI, Git, Statistics",
     ["Built dashboards in Power BI and automated reports with Python and Pandas.",
      "Wrote complex SQL queries for business insights.",
      "Version controlled scripts with Git."],
     ["Sales dashboard.", "A/B test analysis."],
     "B.Com with Data Analytics certificate"),
    ("ML but no SQL or Git",
     "Machine Learning Student",
     "Python, Machine Learning, NLP, Pandas, NumPy, Scikit-learn, Jupyter",
     ["Completed online courses in machine learning and NLP.",
      "Built several notebooks using Pandas and scikit-learn."],
     ["Sentiment classifier on movie reviews.", "Iris and Titanic prediction notebooks."],
     "B.Tech in Mechanical Engineering"),
    ("Backend dev with Python/SQL, no ML",
     "Backend Developer",
     "Python, SQL, Git, Django, Flask, PostgreSQL, Docker, REST API",
     ["Built REST APIs in Django and Flask for an e-commerce platform.",
      "Optimised PostgreSQL queries and wrote Docker deployment files.",
      "Worked in agile teams using Git."],
     ["Inventory management API.", "Authentication service."],
     "B.E. in Computer Engineering"),
    ("Data engineer, little ML",
     "Data Engineer",
     "Python, SQL, Pandas, Git, AWS, Docker, Spark",
     ["Built ETL pipelines in Python and SQL on AWS.",
      "Maintained data warehouse tables and scheduled jobs.",
      "Collaborated with data scientists on feature tables."],
     ["Streaming pipeline with Spark.", "Data quality checker."],
     "B.Tech in Information Technology"),
    ("Statistics background, R-focused",
     "Junior Statistician",
     "R, SQL, Statistics, Excel, Python, Machine Learning, Tableau",
     ["Performed regression and classification modelling in R.",
      "Used SQL for data extraction and Tableau for reporting."],
     ["Customer survey analysis.", "Credit risk scorecard."],
     "M.Sc. in Statistics"),
    ("Aspiring ML, only basic skills",
     "Fresher",
     "Python, Machine Learning, Git, HTML, CSS",
     ["Completed a 6-week Python and machine learning bootcamp."],
     ["Simple linear regression app.", "Personal portfolio website."],
     "B.Tech in Computer Science"),
    ("Software dev, some NLP exposure",
     "Software Engineer",
     "Java, Python, SQL, Git, NLP, Spring Boot, MySQL",
     ["Developed Java microservices for a banking client.",
      "Prototyped a chatbot using NLP libraries during a hackathon.",
      "Wrote SQL for reports."],
     ["Hackathon chatbot.", "Library management system in Java."],
     "B.E. in Computer Science"),
    ("Analytics with ML but no Python depth",
     "Business Analyst",
     "SQL, Excel, Power BI, Tableau, Machine Learning, Statistics, Pandas",
     ["Analysed sales data in SQL and Excel; built Power BI reports.",
      "Applied basic machine learning for customer churn with guidance from the data team."],
     ["Churn analysis.", "Revenue forecasting."],
     "MBA in Analytics"),
    ("Old ML experience, rusty",
     "Software Consultant",
     "Python, SQL, Machine Learning, Git, Java, Excel",
     ["Worked 6 years in IT consulting, mostly on Java applications.",
      "Built one machine learning proof-of-concept for a client in 2019."],
     ["Predictive maintenance PoC."],
     "B.E. in Electronics"),
    ("Keyword-light but relevant",
     "Research Assistant",
     "Python, Pandas, Git, Jupyter, Text Mining, SQL",
     ["Analysed survey text and social media posts using Python and text mining techniques.",
      "Organised datasets with SQL and Pandas."],
     ["Twitter topic analysis.", "Linguistics corpus tool."],
     "M.A. in Computational Linguistics"),
]

POOR = [
    ("Web developer, no data skills",
     "Frontend Developer",
     "HTML, CSS, JavaScript, React, Node.js, Git, Figma",
     ["Built responsive websites for 10+ clients using React and CSS.",
      "Collaborated with designers and used Git for version control."],
     ["Portfolio site.", "E-commerce frontend."],
     "B.Sc. in Information Technology"),
    ("Digital marketer",
     "Digital Marketing Executive",
     "SEO, Google Ads, Content Marketing, Excel, Canva, Social Media",
     ["Managed ad campaigns with a monthly budget of Rs. 5 lakh.",
      "Grew organic traffic by 60% through SEO."],
     ["Brand awareness campaign.", "Email newsletter strategy."],
     "BBA in Marketing"),
    ("Accountant",
     "Accounts Executive",
     "Tally, Excel, GST, Accounting, Bookkeeping, Taxation",
     ["Prepared monthly financial statements and GST returns.",
      "Managed accounts payable and receivable."],
     ["Audit support project."],
     "B.Com"),
    ("Mechanical engineer",
     "Mechanical Design Engineer",
     "AutoCAD, SolidWorks, CATIA, ANSYS, GD&T, Manufacturing",
     ["Designed components for automotive assemblies using SolidWorks.",
      "Ran stress simulations in ANSYS."],
     ["Gearbox design.", "Heat exchanger analysis."],
     "B.E. in Mechanical Engineering"),
    ("HR professional",
     "HR Executive",
     "Recruitment, Onboarding, Payroll, Communication, MS Office, Employee Engagement",
     ["Screened 100+ resumes per week and coordinated interviews.",
      "Managed onboarding for new joiners."],
     ["Employee engagement survey."],
     "MBA in Human Resources"),
    ("Graphic designer",
     "Graphic Designer",
     "Photoshop, Illustrator, Figma, Branding, Typography, Canva",
     ["Created brand identities and social media creatives for startups."],
     ["Logo redesign.", "Packaging design."],
     "B.Des in Visual Communication"),
    ("Keyword-stuffed but no substance",
     "Sales Associate",
     "Python, SQL, Machine Learning, NLP, Pandas, Git, Sales, Customer Service, Excel",
     ["Handled retail customers and achieved monthly sales targets.",
      "Maintained stock registers in Excel."],
     ["Store layout improvement."],
     "B.A. in Economics"),
    ("Civil engineer",
     "Site Engineer",
     "AutoCAD, Revit, Project Management, Estimation, Site Supervision",
     ["Supervised construction of residential buildings.",
      "Prepared cost estimates and BOQs."],
     ["Bridge design study."],
     "B.E. in Civil Engineering"),
    ("Android developer, no data",
     "Android Developer",
     "Java, Kotlin, Android Studio, Firebase, Git, REST API",
     ["Built and published two Android apps with over 50k downloads.",
      "Integrated REST APIs and Firebase."],
     ["Expense tracker app.", "Fitness app."],
     "B.Tech in Computer Science"),
    ("Content writer",
     "Content Writer",
     "Copywriting, Blogging, SEO, Editing, WordPress, Research",
     ["Wrote 200+ blog articles for technology and finance clients.",
      "Edited and proofread marketing material."],
     ["Company blog revamp."],
     "B.A. in English"),
]

ALL = [(g, "Good") for g in GOOD] + [(m, "Maybe") for m in MAYBE] + [(p, "Poor") for p in POOR]
random.shuffle(ALL)   # so filename order does not reveal the label


def make_resume(idx, arch, label):
    name_f, name_l = random.choice(FIRST), random.choice(LAST)
    note, title, skills, exp, proj, degree = arch
    city = random.choice(CITIES)
    doc = Document()
    doc.add_heading(f"{name_f} {name_l}", level=0)
    doc.add_paragraph(f"{title} | {city}, India | {name_f.lower()}.{name_l.lower()}@example.com | +91 90000 {random.randint(10000, 99999)}")

    doc.add_heading("SUMMARY", level=1)
    years = random.choice(["Entry-level", "2 years of experience as", "3 years of experience as", "Final-year student aspiring to be"])
    doc.add_paragraph(f"{years} {title}. Motivated, detail-oriented and eager to learn.")

    doc.add_heading("SKILLS", level=1)
    doc.add_paragraph(skills)

    doc.add_heading("EXPERIENCE", level=1)
    for b in exp:
        doc.add_paragraph(b, style="List Bullet")

    doc.add_heading("PROJECTS", level=1)
    for b in proj:
        doc.add_paragraph(b, style="List Bullet")

    doc.add_heading("EDUCATION", level=1)
    doc.add_paragraph(f"{degree}, {random.choice(['University of Pune', 'VJTI Mumbai', 'NIT Nagpur', 'JNTU Hyderabad'])}, {random.randint(2016, 2026)}")

    fname = f"Candidate_{idx:02d}.docx"
    doc.save(OUT / fname)
    return fname, label, note


rows = [make_resume(i + 1, arch, label) for i, (arch, label) in enumerate(ALL)]

with open("data/labels.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "label", "note"])
    w.writerows(rows)

counts = {l: sum(1 for r in rows if r[1] == l) for l in ("Good", "Maybe", "Poor")}
print(f"Created {len(rows)} resumes in {OUT}/  {counts}")
print("Answer key saved to data/labels.csv")
