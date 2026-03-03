import streamlit as st
import json
from pypdf import PdfReader# PDF text extraction

# Load job roles and core skills
with open("job_roles.json", "r") as f:
    JOB_ROLES = json.load(f)

st.title("📄 Advanced AI Resume Analyzer")
st.write("Upload your resume and get ATS score, missing skills, and professional improvement suggestions.")

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
# Analyze skills
def analyze_resume(resume_text, skills):
    found = [s for s in skills if s.lower() in resume_text]
    missing = [s for s in skills if s.lower() not in resume_text]
    score = int((len(found) / len(skills)) * 100) if skills else 0
    return found, missing, score

# Extract keywords from JD
def extract_keywords(text):
    return [w.strip().lower() for w in text.split() if len(w) > 4]

# Generate professional resume suggestions
def generate_suggestions(found, missing, score):
    suggestions = []

    if score < 50:
        suggestions.append("Your resume score is low. Focus on adding technical projects and quantifiable achievements.")
    elif score < 70:
        suggestions.append("Good resume, but you still need to strengthen missing skills and add measurable results.")
    else:
        suggestions.append("Your resume is strong. Only small improvements are needed.")

    if missing:
        suggestions.append("You can improve your resume by adding these important skills **IF you actually have experience with them**:")
        suggestions.append(", ".join(missing))

    suggestions.append("Use action verbs like: *Designed, Implemented, Led, Automated, Developed, Analyzed*.")
    suggestions.append("Make your project descriptions measurable. Example: 'Improved model accuracy by 18%'.")
    suggestions.append("Ensure your resume has clean formatting, consistent fonts, and proper spacing.")
    suggestions.append("Mention tools, frameworks, certifications, and real results instead of generic statements.")

    return suggestions


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
    st.write(missing if missing else "No missing skills — well done!")

    # NEW FEATURE — Professional Suggestions
    st.subheader("📝 Professional Improvement Suggestions")
    suggestions = generate_suggestions(found, missing, score)
    for s in suggestions:
        st.write("- " + s)
