import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import re

# ==============================
# CONFIGURATION
# ==============================

import os
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 🔐 Secure GitHub Token (DO NOT hardcode token in code)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if GITHUB_TOKEN:
    HEADERS = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
else:
    HEADERS = {
        "Accept": "application/vnd.github.v3+json"
    }

st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")


# ==============================
# UTILITY FUNCTIONS
# ==============================

def extract_username(url):
    """
    Extract username from GitHub URL
    """
    if "github.com/" in url:
        return url.rstrip("/").split("/")[-1]
    return url.strip()


def get_user_data(username):
    """
    Fetch basic user profile data
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_repositories(username):
    """
    Fetch public repositories (up to 100)
    """
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        return []


def check_readme(owner, repo):
    """
    Check if repository has a README file
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    headers = HEADERS.copy()
    headers["Accept"] = "application/vnd.github.v3.raw"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None


# ==============================
# SCORING ENGINE
# ==============================

def calculate_scores(user, repos):

    documentation_score = 0
    activity_score = 0
    repo_quality_score = 0
    technical_depth_score = 0
    impact_score = 0

    total_repos = len(repos)
    readme_count = 0
    recent_active_repos = 0
    languages = set()
    stars = 0
    forks = 0
    repo_scores = []

    six_months_ago = datetime.now().timestamp() - (6 * 30 * 24 * 60 * 60)

    for repo in repos:
        owner = repo["owner"]["login"]
        name = repo["name"]

        # Documentation
        readme = check_readme(owner, name)
        if readme:
            readme_count += 1
            if len(readme) > 300:
                documentation_score += 2
            if "installation" in readme.lower():
                documentation_score += 1
            if "usage" in readme.lower():
                documentation_score += 1
            if "features" in readme.lower():
                documentation_score += 1

        # Activity
        updated_at = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        if updated_at.timestamp() > six_months_ago:
            recent_active_repos += 1

        # Repo Quality
        if repo["description"]:
            repo_quality_score += 1
        if repo["license"]:
            repo_quality_score += 1
        if repo["topics"]:
            repo_quality_score += 1

        # Technical Depth
        if repo["language"]:
            languages.add(repo["language"])

        stars += repo["stargazers_count"]
        forks += repo["forks_count"]

        repo_scores.append(
            (repo["name"], repo["stargazers_count"] + repo["forks_count"])
        )

    # Normalize Documentation
    documentation_score = min(20, documentation_score)

    # Activity Score
    if recent_active_repos > 10:
        activity_score = 20
    elif recent_active_repos > 5:
        activity_score = 15
    elif recent_active_repos > 2:
        activity_score = 10
    elif recent_active_repos > 0:
        activity_score = 5
    else:
        activity_score = 0

    # Normalize Repo Quality
    repo_quality_score = min(20, repo_quality_score)

    # Technical Depth Score
    if len(languages) >= 5:
        technical_depth_score = 20
    elif len(languages) >= 3:
        technical_depth_score = 15
    elif len(languages) >= 2:
        technical_depth_score = 10
    elif len(languages) == 1:
        technical_depth_score = 5
    else:
        technical_depth_score = 0

    # Impact Score (Professional Scaling)
    total_impact = stars + forks
    if total_impact > 100:
        impact_score = 20
    elif total_impact > 50:
        impact_score = 15
    elif total_impact > 10:
        impact_score = 10
    elif total_impact > 0:
        impact_score = 5
    else:
        impact_score = 0

    total_score = (
        documentation_score
        + activity_score
        + repo_quality_score
        + technical_depth_score
        + impact_score
    )

    top_repos = sorted(repo_scores, key=lambda x: x[1], reverse=True)[:3]

    return {
        "Documentation": documentation_score,
        "Activity": activity_score,
        "Repository Quality": repo_quality_score,
        "Technical Depth": technical_depth_score,
        "Impact": impact_score,
        "Total": total_score,
        "Languages": list(languages),
        "Readme Count": readme_count,
        "Recent Activity": recent_active_repos,
        "Top Repos": top_repos,
    }


# ==============================
# FEEDBACK ENGINE
# ==============================

def generate_feedback(scores, total_repos):

    suggestions = []
    red_flags = []

    if scores["Documentation"] < 10:
        suggestions.append("Improve README structure with Installation, Usage, and Features sections.")

    if scores["Activity"] < 10:
        suggestions.append("Increase commit consistency. Recruiters value active contributors.")

    if scores["Repository Quality"] < 10:
        suggestions.append("Add descriptions, topics, and licenses to repositories.")

    if scores["Technical Depth"] < 10:
        suggestions.append("Build projects using diverse technologies (APIs, databases, deployment).")

    if scores["Impact"] < 5:
        suggestions.append("Deploy and share projects to gain visibility and real-world traction.")

    if total_repos < 5:
        suggestions.append("Add more high-quality projects to strengthen your portfolio.")

    if scores["Recent Activity"] == 0:
        red_flags.append("No activity in last 6 months.")

    if scores["Readme Count"] < 2:
        red_flags.append("Very few repositories have proper documentation.")

    if len(scores["Languages"]) == 1:
        red_flags.append("Limited technology diversity.")

    return suggestions, red_flags


# ==============================
# UI
# ==============================

st.title("🚀 GitHub Portfolio Analyzer")
st.write("Analyze your GitHub profile like a recruiter.")

github_url = st.text_input("Enter GitHub Profile URL")

if st.button("Analyze Profile"):

    username = extract_username(github_url)
    user = get_user_data(username)
    repos = get_repositories(username)

    if not user:
        st.error("Invalid username or API limit reached.")
    else:

        scores = calculate_scores(user, repos)
        suggestions, red_flags = generate_feedback(scores, len(repos))

        # Profile Overview
        st.image(user["avatar_url"], width=120)
        st.subheader(user["name"] if user["name"] else username)
        st.write("Followers:", user["followers"])
        st.write("Public Repositories:", user["public_repos"])
        st.write("Bio:", user["bio"])

        # Recruiter Verdict
        if scores["Total"] >= 80:
            verdict = "🟢 Hire Ready"
        elif scores["Total"] >= 60:
            verdict = "🟡 Almost There"
        else:
            verdict = "🔴 Needs Improvement"

        st.subheader("Recruiter Verdict")
        st.success(verdict)

        # Score Display
        st.metric("GitHub Portfolio Score (Out of 100)", scores["Total"])

        df = pd.DataFrame({
            "Category": ["Documentation", "Activity", "Repository Quality", "Technical Depth", "Impact"],
            "Score": [
                scores["Documentation"],
                scores["Activity"],
                scores["Repository Quality"],
                scores["Technical Depth"],
                scores["Impact"],
            ],
        })

        st.bar_chart(df.set_index("Category"))

        # Strength Indicators
        st.subheader("💪 Strength Indicators")
        st.write("Languages Used:", ", ".join(scores["Languages"]))
        st.write("Repositories with README:", scores["Readme Count"])
        st.write("Recently Active Repositories:", scores["Recent Activity"])

        # Top Repositories
        st.subheader("🌟 Top 3 Highlight Repositories")
        for repo in scores["Top Repos"]:
            st.write(f"{repo[0]} (Impact Score: {repo[1]})")

        # Recommendations
        st.subheader("📌 Actionable Recommendations")
        for s in suggestions:
            st.write("•", s)

        # Red Flags
        if red_flags:
            st.subheader("🚨 Recruiter Red Flags")
            for flag in red_flags:
                st.error(flag)

        # AI-Style Summary
        st.subheader("🧠 Recruiter Summary")
        summary = f"""
This profile demonstrates experience in {', '.join(scores['Languages'])}.
Overall portfolio strength is categorized as {verdict}.
Improving documentation clarity and real-world deployment exposure
would significantly increase recruiter attractiveness.
"""
        st.write(summary)
