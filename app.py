import streamlit as st
from dotenv import load_dotenv
from src.config import AppConfig
from src.file_parser import parse_uploaded_file
from src.resume_analyzer import analyze_resume, generate_cover_letter
from src.report_generator import build_markdown_report

load_dotenv()

st.set_page_config(page_title="AI Resume Optimizer", page_icon="🧠", layout="wide")
st.title("🧠 AI Resume Optimizer")
st.caption("Analyze your resume against a target job description and generate practical improvements.")

config = AppConfig.from_env()

with st.sidebar:
    st.header("Settings")
    st.write(f"Model: `{config.openai_model}`")
    st.divider()
    st.write("Tip: Use the full job description for better results.")

uploaded_resume = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])

resume_text_input = st.text_area(
    "Or paste your resume text here",
    height=220,
    placeholder="Paste resume content...",
)

job_description = st.text_area(
    "Paste the target job description",
    height=260,
    placeholder="Paste job description...",
)

resume_text = ""

if uploaded_resume is not None:
    try:
        resume_text = parse_uploaded_file(uploaded_resume)
        st.success(f"Parsed uploaded file: {uploaded_resume.name}")
    except Exception as exc:
        st.error(f"Could not parse file: {exc}")

if resume_text_input.strip():
    resume_text = resume_text_input.strip()

if st.button("Analyze Resume", type="primary"):
    if not config.openai_api_key:
        st.error("Missing OPENAI_API_KEY. Please create a .env file and add your API key.")
        st.stop()
    if not resume_text.strip():
        st.error("Please upload or paste your resume.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste a target job description.")
        st.stop()

    with st.spinner("Analyzing resume..."):
        result = analyze_resume(resume_text, job_description, config.openai_model)

    st.session_state["analysis_result"] = result
    st.session_state["resume_text"] = resume_text
    st.session_state["job_description"] = job_description

if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    st.divider()
    st.subheader("Analysis Results")
    st.metric("Overall Match Score", f"{result.get('overall_match_score', 0)}/100")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Matched Skills")
        for skill in result.get("matched_skills", []):
            st.success(skill)
    with col2:
        st.markdown("### Missing or Weak Skills")
        for skill in result.get("missing_skills", []):
            st.warning(skill)

    st.markdown("### Job Requirements Summary")
    for item in result.get("job_requirements_summary", []):
        st.write(f"- {item}")

    st.markdown("### Weak Resume Bullets")
    weak_bullets = result.get("weak_resume_bullets", [])
    if weak_bullets:
        for bullet in weak_bullets:
            st.write(f"- {bullet}")
    else:
        st.info("No weak bullet points identified.")

    st.markdown("### Improved Resume Bullets")
    for item in result.get("improved_resume_bullets", []):
        if isinstance(item, dict):
            st.markdown("**Original:**")
            st.write(item.get("original", ""))
            st.markdown("**Improved:**")
            st.write(item.get("improved", ""))
            st.divider()
        else:
            st.write(f"- {item}")

    st.markdown("### Suggested Professional Summary")
    st.info(result.get("suggested_summary", ""))

    st.markdown("### Action Plan")
    for item in result.get("action_plan", []):
        st.write(f"- {item}")

    report = build_markdown_report(result)
    st.download_button("Download Markdown Report", report, "resume_optimization_report.md", "text/markdown")

    st.divider()
    st.subheader("Optional: Generate Cover Letter")
    if st.button("Generate Cover Letter"):
        with st.spinner("Generating cover letter..."):
            cover_letter = generate_cover_letter(
                st.session_state["resume_text"],
                st.session_state["job_description"],
                result,
                config.openai_model,
            )
        st.markdown(cover_letter)
        st.download_button("Download Cover Letter", cover_letter, "cover_letter.md", "text/markdown")
