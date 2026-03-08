import streamlit as st
import json
from PyPDF2 import PdfReader

# Load job roles and core skills
with open("job_roles.json", "r") as f:
    JOB_ROLES = json.load(f)

st.title("📄 Advanced AI Resume Analyzer")
st.write("Upload your resume and get ATS score, missing skills, and professional improvement suggestions.")

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content.lower()   # convert to lowercase for accuracy
    return text

# Analyze skills
def analyze_resume(resume_text, skills):
    resume_text = resume_text.lower()
    found = [s for s in skills if s.lower() in resume_text]
    missing = [s for s in skills if s.lower() not in resume_text]
    score = int((len(found) / len(skills)) * 100) if skills else 0
    return found, missing, score

# Extract keywords from JD
def extract_keywords(text):
    return [w.strip().lower() for w in text.split() if len(w) > 4]

# Professional Suggestions
def generate_suggestions(found, missing, score):
    suggestions = []

    if score < 50:
        suggestions.append("Your resume score is low. Focus on adding technical projects and quantifiable achievements.")
    elif score < 70:
        suggestions.append("Good resume, but you still need to strengthen missing skills and add measurable results.")
    else:
        suggestions.append("Your resume is strong. Only small improvements are needed.")

    if missing:
        suggestions.append("Add these important skills (only if you truly have experience):")
        suggestions.append(", ".join(missing))

    suggestions.append("Use action verbs like: Designed, Implemented, Led, Automated, Developed, Analyzed.")
    suggestions.append("Make projects measurable. Example: 'Improved model accuracy by 18%'.")
    suggestions.append("Ensure formatting is clean, consistent, and well-structured.")
    suggestions.append("Highlight tools, frameworks, and certifications.")

    return suggestions


# ---------------- UI --------------------

uploaded = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
selected_role = st.selectbox("Select Job Role (Optional)", ["None"] + list(JOB_ROLES.keys()))
jd_input = st.text_area("Paste Job Description (Optional)")

if uploaded:
    resume_text = extract_text_from_pdf(uploaded)
    
    st.success("Resume uploaded successfully!")

    role_skills = JOB_ROLES[selected_role] if selected_role != "None" else []
    jd_keywords = extract_keywords(jd_input) if jd_input else []

    combined_keywords = list(set(role_skills + jd_keywords))

    found, missing, score = analyze_resume(resume_text, combined_keywords)

    st.subheader("📊 ATS Match Score")
    st.metric("Match Percentage", f"{score}%")

    st.subheader("✅ Skills Identified in Resume")
    st.write(found if found else "No important skills detected.")

    st.subheader("❌ Missing Important Skills")
    st.write(missing if missing else "No missing skills — great job!")

    st.subheader("📝 Professional Improvement Suggestions")
    suggestions = generate_suggestions(found, missing, score)
    for s in suggestions:
        st.write("- " + s)
