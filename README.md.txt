# 🚀 GitHub Portfolio Analyzer

Analyze GitHub profiles like a recruiter and generate an objective
GitHub Portfolio Score with actionable feedback.

------------------------------------------------------------------------

## 🔍 Problem Statement

For many students and early-career developers, GitHub serves as their
primary technical portfolio. However, most GitHub profiles fail to
effectively communicate:

-   Real technical depth
-   Consistent contribution history
-   Clear documentation
-   Project impact
-   Real-world relevance

A strong GitHub profile can open doors. A weak one silently closes them.

------------------------------------------------------------------------

## 💡 Solution

GitHub Portfolio Analyzer:

1.  Accepts a GitHub profile URL\
2.  Fetches public repository data using GitHub API\
3.  Analyzes repository structure and activity\
4.  Generates a structured GitHub Portfolio Score (Out of 100)\
5.  Highlights strengths and recruiter red flags\
6.  Provides actionable improvement suggestions

------------------------------------------------------------------------

## 🎯 Key Features

-   Structured Portfolio Score (Out of 100)
-   Recruiter Verdict Badge
-   Documentation Quality Analysis
-   Activity Consistency Check
-   Technical Depth Detection
-   Impact Score (Stars + Forks)
-   Top 3 Highlight Repositories
-   Recruiter Red Flags Detection
-   Actionable Recommendations

------------------------------------------------------------------------

## 📊 Scoring Dimensions

  Category                Max Score
  ----------------------- -----------
  Documentation Quality   20
  Activity Consistency    20
  Repository Quality      20
  Technical Depth         20
  Project Impact          20
  **Total**               **100**

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Python
-   Streamlit
-   GitHub REST API
-   Requests
-   Python-dotenv
-   Pandas

------------------------------------------------------------------------

## ▶️ How to Run Locally

1.  Clone the repository

```{=html}
<!-- -->
```
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

2.  Navigate into project

```{=html}
<!-- -->
```
    cd YOUR_REPO_NAME

3.  Create virtual environment

```{=html}
<!-- -->
```
    python -m venv venv
    venv\Scripts\activate

4.  Install dependencies

```{=html}
<!-- -->
```
    pip install streamlit requests pandas python-dotenv

5.  Create `.env` file

```{=html}
<!-- -->
```
    GITHUB_TOKEN=your_token_here

6.  Run application

```{=html}
<!-- -->
```
    streamlit run app.py


## 🎯 Impact

This tool helps students: - Understand recruiter expectations - Improve
GitHub presentation - Become hiring-ready


