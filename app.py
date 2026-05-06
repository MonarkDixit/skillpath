# =============================================================================
# app.py
# SkillPath: Career Skill Dependency Mapper
# Author: Monark Dixit (UID: 122259645)
# Course: MSML606, Spring 2026
#
# PURPOSE:
#   Streamlit frontend for SkillPath. Two-page layout:
#     Page 1 (Home): Role selector and skill checklist
#     Page 2 (Results): Full roadmap with explanations for each section
#
# HOW TO RUN:
#   streamlit run app.py
#
# NOTE: AI assistance was used to generate this UI file only.
#       All core algorithm files were written manually.
# =============================================================================

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.engine import build_base_graph, get_roadmap
from src.data_loader import build_role_skills_map, get_all_roles, get_all_skills


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="SkillPath",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# CSS
# =============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --black:    #0d0d0d;
    --white:    #fafafa;
    --red:      #c0392b;
    --red-lite: #fdf2f2;
    --g100:     #f5f5f5;
    --g200:     #e8e8e8;
    --g400:     #aaaaaa;
    --g600:     #555555;
    --r: 14px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--white);
    font-family: 'DM Sans', sans-serif;
    color: var(--black);
}

#MainMenu, footer, header { visibility: hidden; }

.main .block-container {
    padding: 2.5rem 3rem 5rem 3rem;
    max-width: 1080px;
}

/* HEADER */
.header {
    border-bottom: 1.5px solid var(--g200);
    padding-bottom: 1.8rem;
    margin-bottom: 2.5rem;
}
.wordmark {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    letter-spacing: -0.03em;
    line-height: 1;
    color: var(--black);
}
.wordmark em { color: var(--red); font-style: normal; }
.tagline { font-size: 1rem; color: var(--g600); margin-top: 0.45rem; font-weight: 400; }
.byline {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--g400);
    margin-top: 0.9rem;
    letter-spacing: 0.07em;
}

/* LABELS */
.lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--g400);
    display: block;
    margin-bottom: 0.65rem;
}

/* CARDS */
.card {
    border: 1.5px solid var(--g200);
    border-radius: var(--r);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    background: var(--white);
}
.card-dark {
    background: var(--black);
    border: none;
    border-radius: var(--r);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* COVERAGE */
.big-pct {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: var(--red);
    line-height: 1;
}
.pct-sub { font-size: 0.85rem; color: var(--g600); margin-top: 0.3rem; }
.bar-track {
    background: var(--g100);
    border-radius: 999px;
    height: 10px;
    margin: 0.8rem 0 0.3rem;
    overflow: hidden;
}
.bar-fill { height: 100%; border-radius: 999px; background: var(--red); }

/* SECTION EXPLAINER */
.explainer {
    font-size: 0.88rem;
    color: var(--g600);
    line-height: 1.7;
    margin-bottom: 1.2rem;
    padding: 1rem 1.2rem;
    background: var(--g100);
    border-radius: var(--r);
    border-left: 3px solid var(--red);
}

/* ROADMAP */
.step {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    padding: 0.85rem 0;
    border-bottom: 1px solid var(--g100);
}
.step:last-child { border-bottom: none; }
.step-n {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: var(--black);
    color: var(--white);
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step-name { font-size: 0.92rem; font-weight: 500; color: var(--black); flex: 1; }
.pill {
    font-family: 'DM Mono', monospace;
    font-size: 0.63rem;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    flex-shrink: 0;
}
.pill-red { background: var(--red-lite); color: var(--red); border: 1px solid #f5c6c6; }

/* CHIPS */
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.chip {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    border: 1.5px solid var(--black);
    background: var(--black);
    color: var(--white);
}

/* FREQ BARS */
.fbar { margin-bottom: 0.7rem; }
.fbar-top {
    display: flex;
    justify-content: space-between;
    font-size: 0.82rem;
    color: var(--g600);
    margin-bottom: 0.22rem;
}
.fbar-num { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: var(--g400); }
.fbar-track { background: var(--g100); border-radius: 999px; height: 6px; }
.fbar-fill { height: 100%; border-radius: 999px; background: var(--red); }

/* STATS */
.srow {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--g200);
}
.srow:last-child { border-bottom: none; }
.sk { font-size: 0.82rem; color: var(--g400); }
.sv { font-family: 'DM Mono', monospace; font-size: 0.82rem; color: var(--black); font-weight: 500; }

/* HOW STEPS */
.how { display: flex; gap: 0.8rem; align-items: flex-start; margin-bottom: 0.85rem; }
.how-n {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: var(--red-lite);
    border: 1px solid #f5c6c6;
    color: var(--red);
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
}
.how-t { font-size: 0.83rem; color: var(--g600); line-height: 1.55; }

/* EMPTY */
.empty { text-align: center; padding: 4rem 2rem; }
.empty-i { font-size: 2.2rem; color: var(--g200); margin-bottom: 1rem; }
.empty-h {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: var(--g400);
    margin-bottom: 0.4rem;
}
.empty-s { font-size: 0.85rem; color: var(--g400); line-height: 1.6; }

/* RESULTS PAGE HEADER */
.results-header {
    border-bottom: 1.5px solid var(--g200);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}
.results-role {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: var(--black);
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.results-role em { color: var(--red); font-style: normal; }
.results-sub { font-size: 0.92rem; color: var(--g600); margin-top: 0.4rem; }

/* STREAMLIT OVERRIDES */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: 10px !important;
    border-color: var(--g200) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button {
    background: var(--black) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    -webkit-text-fill-color: #fff !important;
}
.stButton > button:hover { background: var(--red) !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CACHED LOADERS
# =============================================================================

@st.cache_resource(show_spinner=False)
def load_data():
    role_skills_map = build_role_skills_map()
    graph = build_base_graph()
    all_roles = get_all_roles(role_skills_map)
    all_skills = get_all_skills(role_skills_map)
    return role_skills_map, graph, all_roles, all_skills


# =============================================================================
# HELPERS
# =============================================================================

def freq_bar(skill: str, count: int, max_count: int) -> str:
    pct = int(count / max_count * 100) if max_count else 0
    return f"""
    <div class="fbar">
        <div class="fbar-top">
            <span>{skill}</span>
            <span class="fbar-num">{count} job listings</span>
        </div>
        <div class="fbar-track">
            <div class="fbar-fill" style="width:{pct}%"></div>
        </div>
    </div>"""


def roadmap_step(rank: int, skill: str) -> str:
    return f"""
    <div class="step">
        <div class="step-n">{rank}</div>
        <div class="step-name">{skill.title()}</div>
        <span class="pill pill-red">learn this</span>
    </div>"""


# =============================================================================
# PAGE 1: HOME
# =============================================================================

def render_home(role_skills_map, graph, all_roles, all_skills):

    st.markdown("""
    <div class="header">
        <div class="wordmark">Skill<em>Path</em></div>
        <div class="tagline">
            Tell us what job you want. We show you exactly what to learn and in what order.
        </div>
        <div class="byline">MSML606 &nbsp;·&nbsp; SPRING 2026 &nbsp;·&nbsp; MONARK DIXIT</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.55], gap="large")

    with left:
        st.markdown('<span class="lbl">Step 1 &nbsp;— What job do you want?</span>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.8rem;color:#aaa;margin-bottom:0.5rem;">Popular choices:</div>
        """, unsafe_allow_html=True)

        quick_roles = {
            "Sales Manager": "sales manager",
            "Data Analyst": "data analyst",
            "Marketing Manager": "marketing manager",
            "Project Manager": "project manager",
        }

        col1, col2 = st.columns(2)
        for i, (label, role_val) in enumerate(quick_roles.items()):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(label, key=f"quick_{role_val}"):
                    st.session_state["_preset_role"] = role_val

        preset = st.session_state.get("_preset_role", None)
        default_idx = 0
        if preset and preset in all_roles:
            default_idx = all_roles.index(preset)
        elif "data analyst" in all_roles:
            default_idx = all_roles.index("data analyst")

        selected_role = st.selectbox(
            "Or search all roles",
            options=all_roles,
            index=default_idx,
            label_visibility="visible",
        )

        st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<span class="lbl">Step 2 &nbsp;— What do you already know?</span>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.82rem;color:#888;margin-bottom:0.6rem;line-height:1.5;">
            Select any skills you already have. Do not worry if you are unsure,
            you can always come back and change this.
        </div>
        """, unsafe_allow_html=True)

        role_req = set(role_skills_map.get(selected_role, []))
        graph_skills = sorted(graph.get_all_nodes())
        checklist_skills = sorted(role_req)

        selected_skills = st.multiselect(
            "Your current skills",
            options=checklist_skills,
            default=[],
            label_visibility="collapsed",
            placeholder="Type to search, e.g. python, sql, excel...",
        )

        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

        if st.button("Show Me My Roadmap", use_container_width=True, key="go_btn"):
            with st.spinner("Building your roadmap..."):
                result = get_roadmap(
                    current_skills=selected_skills,
                    target_role=selected_role,
                    role_skills_map=role_skills_map,
                    graph=graph,
                )
                st.session_state.result = result
                st.session_state.role_used = selected_role
                st.session_state.skills_used = selected_skills
                st.session_state.page = "results"
                st.rerun()

        st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<span class="lbl">What is SkillPath?</span>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.85rem;color:#666;line-height:1.7;margin-bottom:1.2rem;">
            Job postings list dozens of required skills but never tell you
            which ones to learn first. SkillPath figures that out for you.
            <br><br>
            It maps out which skills depend on which others, then builds
            a step-by-step learning plan based on what you already know.
        </div>
        """, unsafe_allow_html=True)

        for i, step in enumerate([
            "You pick a job you are aiming for.",
            "You tell us what skills you already have.",
            "We figure out the gap between where you are and where you need to be.",
            "We give you a numbered list of skills to learn, in the right order.",
        ], 1):
            st.markdown(f"""
            <div class="how">
                <div class="how-n">{i}</div>
                <div class="how-t">{step}</div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="empty">
            <div class="empty-i">◈</div>
            <div class="empty-h">Your roadmap will appear on the next page</div>
            <div class="empty-s">
                Pick a role on the left, add the skills you already have,
                and click <strong>Show Me My Roadmap</strong>.
                <br><br>
                <span style="color:#ccc;">
                    Try: Pick "Data Analyst" with no skills to see a full
                    learning plan from scratch.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# PAGE 2: RESULTS
# =============================================================================

def render_results(role_skills_map, graph):
    result = st.session_state.get("result")
    role_used = st.session_state.get("role_used", "")
    skills_used = st.session_state.get("skills_used", [])

    if not result:
        st.session_state.page = "home"
        st.rerun()
        return

    role_display = role_used.title()
    skills_str = (
        ", ".join(s.title() for s in skills_used)
        if skills_used else "no prior skills"
    )

    # Back button at the top
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    # Results page header
    st.markdown(f"""
    <div class="results-header">
        <div class="results-role">Your roadmap to become a <em>{role_display}</em></div>
        <div class="results-sub">
            Starting with: {skills_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Qualified banner
    if result["is_qualified"]:
        st.markdown(f"""
        <div class="card-dark">
            <div style="font-size:1.5rem;margin-bottom:0.5rem;">✓</div>
            <div style="font-family:'DM Serif Display',serif;font-size:1.15rem;
                        color:#fff;margin-bottom:0.3rem;">
                You already qualify for {role_display}
            </div>
            <div style="font-size:0.83rem;color:#777;">
                You have all {len(result['required_skills'])} skills this role needs.
                You are ready to apply.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:

        # --- SECTION 1: Coverage ---
        st.markdown("""
        <div class="explainer">
            <strong>Your skill coverage</strong> shows how much of this role you already
            cover with your current skills. The higher the percentage, the closer you
            are to being ready. A coverage of 100% means you meet every requirement
            employers look for in this role.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <span class="lbl">How close are you to {role_display}?</span>
            <div class="big-pct">{result['coverage_pct']}%</div>
            <div class="pct-sub">
                You have {len(result['already_have'])} out of
                {len(result['required_skills'])} skills this role requires.
            </div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{result['coverage_pct']}%"></div>
            </div>
            <div style="font-size:0.78rem;color:#aaa;margin-top:0.3rem;">
                {"You are fully qualified!" if result['is_qualified']
                 else f"{len(result['missing_skills'])} skill(s) left to close the gap."}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Skills already have
        if result["already_have"]:
            chips_html = "".join(
                f'<span class="chip">{s.title()}</span>'
                for s in result["already_have"]
            )
            st.markdown(f"""
            <div style="margin-bottom:1.4rem;">
                <span class="lbl">Skills you already have ✓</span>
                <div class="chips">{chips_html}</div>
            </div>
            """, unsafe_allow_html=True)

        # --- SECTION 2: Roadmap ---
        st.markdown("""
        <div class="explainer" style="margin-top:1rem;">
            <strong>Your learning roadmap</strong> is a numbered list of skills to learn,
            ordered so that each skill builds naturally on the one before it. You should
            not skip steps because later skills assume you already understand the earlier ones.
            Think of it like a staircase: each step gets you one level closer to your goal.
        </div>
        """, unsafe_allow_html=True)

        if result["roadmap"]:
            steps_html = "".join(
                roadmap_step(i, skill)
                for i, skill in enumerate(result["roadmap"], 1)
            )
            st.markdown(f"""
            <div class="card">
                <span class="lbl">
                    Learn these {len(result['roadmap'])} skill(s) in this order
                </span>
                {steps_html}
            </div>
            """, unsafe_allow_html=True)
        elif result["is_qualified"]:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2rem;">
                <div style="font-family:'DM Serif Display',serif;font-size:1rem;
                            color:#0d0d0d;margin-bottom:0.3rem;">
                    Nothing left to learn for this role.
                </div>
                <div style="font-size:0.83rem;color:#888;">
                    Every skill this role requires is already on your profile.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:

        # --- SECTION 3: Most in-demand skills ---
        st.markdown("""
        <div class="explainer">
            <strong>Most in-demand skills</strong> shows which skills appear most
            frequently across real job listings for this role. The longer the bar,
            the more employers ask for that skill. Use this to prioritize which
            skills will make your profile stand out the most.
        </div>
        """, unsafe_allow_html=True)

        if result["top_skills"]:
            max_c = result["top_skills"][0][1]
            bars_html = "".join(
                freq_bar(s.title(), c, max_c)
                for s, c in result["top_skills"]
            )
            st.markdown(f"""
            <div class="card">
                <span class="lbl">
                    Skills that appear most in {role_display} job listings
                </span>
                {bars_html}
            </div>
            """, unsafe_allow_html=True)

        # --- How SkillPath figured this out ---
        st.markdown("""
        <div class="explainer" style="margin-top:1rem;">
            <strong>How SkillPath works</strong> under the hood: it models all skills
            as a network where some skills are prerequisites for others. It then uses
            two graph algorithms to build your roadmap. First, it finds the shortest
            path from your current skills to the ones you need. Then it sorts them
            into the right learning order so no skill appears before its prerequisites.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <span class="lbl">How SkillPath figured this out</span>
            <div class="srow">
                <span class="sk">Roles in database</span>
                <span class="sv">{len(role_skills_map):,}</span>
            </div>
            <div class="srow">
                <span class="sk">Skills in the dependency map</span>
                <span class="sv">{graph.get_stats()['node_count']}</span>
            </div>
            <div class="srow">
                <span class="sk">Skill relationships mapped</span>
                <span class="sv">{graph.get_stats()['edge_count']}</span>
            </div>
            <div class="srow">
                <span class="sk">Step 1: Find missing skills</span>
                <span class="sv">BFS shortest path</span>
            </div>
            <div class="srow">
                <span class="sk">Step 2: Order them correctly</span>
                <span class="sv">Topological sort</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Back button at the bottom too
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("← Try a different role", key="back_btn_2"):
            st.session_state.page = "home"
            st.rerun()


# =============================================================================
# MAIN ROUTER
# =============================================================================

def main():
    with st.spinner("Loading..."):
        role_skills_map, graph, all_roles, all_skills = load_data()

    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "result" not in st.session_state:
        st.session_state.result = None

    if st.session_state.page == "home":
        render_home(role_skills_map, graph, all_roles, all_skills)
    elif st.session_state.page == "results":
        render_results(role_skills_map, graph)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()