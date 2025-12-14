import streamlit as st
import requests

# ==============================
# CONFIG
# ==============================
BACKEND_URL = "https://repoai.onrender.com/analyze/"

st.set_page_config(
    page_title="Repo Mirror AI",
    page_icon="🔍",
    layout="wide"
)

# ==============================
# HEADER
# ==============================
st.title("🔍 Repo AI")
st.subheader("AI-powered GitHub Repository Evaluation & Improvement Roadmap")

st.markdown(
    """
Analyze any public GitHub repository and get:
- 📊 Quality Score
- 🧠 Professional Summary
- 🛠️ Personalized Improvement Roadmap
"""
)

st.divider()

# ==============================
# INPUT SECTION
# ==============================
repo_url = st.text_input(
    "🔗 Enter GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)

analyze_btn = st.button("🚀 Analyze Repository")

# ==============================
# API CALL
# ==============================
if analyze_btn:
    if not repo_url:
        st.warning("Please enter a GitHub repository URL.")
    else:
        with st.spinner("Analyzing repository... This may take a few seconds."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"repo_url": repo_url},
                    timeout=120
                )

                if response.status_code != 200:
                    st.error(f"Backend error: {response.text}")
                else:
                    data = response.json()

                    # ==============================
                    # SCORE SECTION
                    # ==============================
                    score = data["score"]

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Score", f"{score['total_score']} / 100")
                    col2.metric("Level", score["level"])
                    col3.metric("Badge", score["badge"])

                    st.progress(score["total_score"] / 100)

                    st.divider()
                    
                # ==============================
                # DETAILED PROJECT WORKING
                # ==============================
                st.subheader("📘 Repository Overview & Working")

                overview = data.get("project_overview", {})

                with st.container(border=True):
                
                    st.markdown("### 🎯 Project Purpose")
                    st.write(overview.get("purpose", "Not available"))

                    st.markdown("### ❓ Problem It Solves")
                    st.write(overview.get("problem", "Not available"))

                    st.markdown("### 🧩 Core Components / Modules")
                    components = overview.get("components", [])
                    if components:
                        for comp in components:
                            st.markdown(f"- {comp}")
                    else:
                        st.write("Not specified.")

                    st.markdown("### ⚙️ How the System Works")
                    workflow = overview.get("workflow", [])
                    if workflow:
                        for step in workflow:
                            st.markdown(f"- {step}")
                    else:
                        st.write("Workflow details not available.")

                    st.markdown("### 🚀 Typical Use Case")
                    st.write(overview.get("use_case", "Not specified."))
                    



                    # ==============================
                    # SUMMARY
                    # ==============================
                    st.subheader("🧠 Professional Evaluation Summary")
                    st.write(data["summary"])

                    st.divider()

                    # ==============================
                    # ROADMAP
                    # ==============================
                    st.subheader("🛠️ Personalized Improvement Roadmap")

                    roadmap_items = data["roadmap"]["items"]

                    if not roadmap_items:
                        st.info("No roadmap items generated.")
                    else:
                        for item in roadmap_items:
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                    **Priority {item['priority']} — {item['category']}**

                                    **Action:**  
                                    {item['action']}

                                    **Expected Impact:**  
                                    _{item['expected_impact']}_
                                    """
                                )

                    st.divider()

                    # ==============================
                    # DETAILED ANALYSIS (OPTIONAL)
                    # ==============================
                    with st.expander("📂 Detailed Analysis (For Developers)"):
                        st.json(data["analysis"])

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
