import streamlit as st
import requests
 
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="PathFinder", page_icon="🧭", layout="wide")

st.title("🧭 PathFinder — CV ↔ Job Matching (RAG + LLM)")
st.caption("Upload your resume, paste a job offer, and get an explainable match score with evidence.")


def post_file(endpoint: str, file_bytes: bytes, filename: str, mime: str = "application/pdf"):
    url = f"{API_BASE}{endpoint}"
    files = {"file": (filename, file_bytes, mime)}
    r = requests.post(url, files=files, timeout=120)
    r.raise_for_status()
    return r.json()

def post_json(endpoint: str, payload: dict):
    url = f"{API_BASE}{endpoint}"
    r = requests.post(url, json=payload, timeout=180)
    r.raise_for_status()
    return r.json()

def post_form(endpoint: str, data: dict):
    url = f"{API_BASE}{endpoint}"
    r = requests.post(url, data=data, timeout=180)
    r.raise_for_status()
    return r.json()

st.sidebar.header("Settings")
API_BASE = st.sidebar.text_input("API Base URL", API_BASE)

top_k_resume = st.sidebar.slider("Top K resume chunks", 3, 10, 6)

st.sidebar.markdown("---")
st.sidebar.write("✅ Make sure the API is running:")
st.sidebar.code("python -m uvicorn main:app --reload --port 8000")

        
col1, col2 = st.columns(2)

with col1:
    st.subheader("1) Upload Resume (PDF) → Index")
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if st.button("Index Resume", type="primary", disabled=resume_file is None):
        try:
            with st.spinner("Indexing resume into vector store..."):
                pdf_bytes = resume_file.getvalue()
                out = post_file("/rag/index_resume", pdf_bytes, resume_file.name)
            st.success("Resume indexed successfully ✅")
            st.session_state["resume_indexed"] = True
            st.json(out)
        except requests.HTTPError as e:
            st.error(f"API error: {e.response.text}")
        except Exception as e:
            st.error(str(e))

    st.markdown("---")
    st.subheader("Optional: Quick CV parse preview")
    if st.button("Parse Resume (structure)", disabled=resume_file is None):
        try:
            with st.spinner("Parsing resume..."):
                pdf_bytes = resume_file.getvalue()
                out = post_file("/resume/parse", pdf_bytes, resume_file.name)
            st.json(out)
        except requests.HTTPError as e:
            st.error(f"API error: {e.response.text}")
        except Exception as e:
            st.error(str(e))

with col2:
    st.subheader("2) Paste Job Offer → Upload → Match")
    title = st.text_input("Job title", "Consultant Data Quality Solvabilité 2 H/F")
    company = st.text_input("Company", "Comeetli")
    location = st.text_input("Location", "Paris")

    description = st.text_area(
        "Job description (paste full offer here)",
        height=260,
        placeholder="Paste the full job offer here (multi-line is OK)."
    )

    if st.button("Upload Job Offer", disabled=(not description.strip())):
        try:
            with st.spinner("Uploading & indexing job offer..."):
                payload = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description
                }
                out = post_form("/job/upload_text", payload)
            st.success("Job offer indexed ✅")
            st.session_state["job_id"] = out["job_id"]
            st.write("Job ID:")
            st.code(out["job_id"])
        except requests.HTTPError as e:
            st.error(f"API error: {e.response.text}")
        except Exception as e:
            st.error(str(e))

    st.markdown("---")
    st.subheader("3) Match")
    job_id = st.text_input("Job ID", value=st.session_state.get("job_id", ""))

    if st.button("Run Match", type="primary", disabled=(not job_id.strip())):
        try:
            with st.spinner("Matching job ↔ resume (RAG + LLM)..."):
                payload = {"job_id": job_id.strip(), "top_k_resume": top_k_resume}
                out = post_json("/job/match", payload)

            st.success("Match completed ✅")

            result = out.get("result")
            if result:
                # Pretty metrics
                score = result.get("match_score", 0)
                st.metric("Match score", f"{score}/100")

                cA, cB = st.columns(2)
                with cA:
                    st.write("✅ Strong matches")
                    st.write(result.get("strong_matches", []))
                with cB:
                    st.write("⚠️ Missing skills")
                    st.write(result.get("missing_skills", []))

                st.write("🛠️ Recommended actions")
                st.write(result.get("recommended_actions", []))

                st.write("📌 Evidence")
                st.json(result.get("evidence", {}))

                st.write("📝 Notes")
                st.write(result.get("notes", ""))

                with st.expander("See raw API payload (debug)"):
                    st.json(out)
            else:
                st.warning("LLM output could not be parsed as JSON. Showing raw output:")
                st.code(out.get("raw_llm", ""))
                with st.expander("See raw API payload (debug)"):
                    st.json(out)

        except requests.HTTPError as e:
            st.error(f"API error: {e.response.text}")
        except Exception as e:
            st.error(str(e))
