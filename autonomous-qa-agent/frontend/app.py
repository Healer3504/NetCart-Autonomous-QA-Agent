import streamlit as st
import requests
from pathlib import Path

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NetCart QA Agent", page_icon="🧠", layout="wide")

# -------------------------------------------------------
# Load CSS (FIXED — defined BEFORE calling)
# -------------------------------------------------------
def local_css(filename: str):
    filename = Path(filename)
    if not filename.exists():
        st.error(f"CSS file not found: {filename}")
        return
    with open(filename, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = Path(__file__).parent / "netflix_theme.css"
local_css(css_path)

# -------------------------------------------------------
# HEADER UI
# -------------------------------------------------------
st.markdown("""
<div class="topbar">
  <div class="brand">Net<span class="brand-red">Cart</span> — QA Agent</div>
  <div class="subtitle">Upload → Build KB → Generate Tests → Export Selenium</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# UPLOAD DOCUMENT SECTION
# -------------------------------------------------------
st.markdown("### Upload any document (PDF, PPTX, DOCX, TXT, Images) — Live Upload")

uploaded_file = st.file_uploader(
    "Upload a file",
    type=["pdf", "ppt", "pptx", "docx", "txt", "csv", "png", "jpg", "jpeg","md" , "json"]
)

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")

    if st.button("Send to Backend & Upload"):
        files = {
            "files": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        with st.spinner("Uploading file to backend…"):
            resp = requests.post(f"{BACKEND_URL}/upload_docs", files=files)

        st.write(resp.json())

# -------------------------------------------------------
# BUILD KNOWLEDGE BASE
# -------------------------------------------------------
st.markdown("---")
st.markdown("### Build Knowledge Base")

if st.button("Build KB"):
    with st.spinner("Building KB…"):
        resp = requests.post(f"{BACKEND_URL}/build_kb")
    st.write(resp.json())

# -------------------------------------------------------
# GENERATE TEST CASES
# -------------------------------------------------------
st.markdown("---")
st.markdown("### Generate Test Cases")

prompt = st.text_area("Describe what tests you want:", height=120)

if st.button("Generate Test Cases"):
    if not prompt.strip():
        st.warning("Please enter a test prompt.")
    else:
        with st.spinner("Generating tests…"):
            resp = requests.post(f"{BACKEND_URL}/generate_tests", json={"prompt": prompt})
        st.write(resp.json())
        if "tests" in resp.json():
            st.session_state["latest_tests"] = resp.json()["tests"]

# -------------------------------------------------------
# SHOW TEST CASES + SELENIUM EXPORT
# -------------------------------------------------------
tests = st.session_state.get("latest_tests", [])

if tests:
    st.markdown("### Generated Test Cases")

    for idx, test in enumerate(tests):
        st.json(test)  # OLD WAY

        if st.button(f"Generate Selenium Script #{idx+1}"):

# -------------------------------------------------------
# SIDEBAR HEALTH CHECK
# -------------------------------------------------------
st.sidebar.header("Backend Status")
try:
    health = requests.get(f"{BACKEND_URL}/health").json()
    st.sidebar.success("Backend Running ✔")
    st.sidebar.write(health)
except:
    st.sidebar.error("Backend Offline ✘")
