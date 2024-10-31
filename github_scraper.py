# Install necessary libraries in Colab
pip install requests
pip install pandas

import requests
import pandas as pd
import os

# Set your GitHub username and token as environment variables for security.
os.environ['GITHUB_USERNAME'] = 'riya360-arch'
os.environ['GITHUB_TOKEN'] = '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'

# GitHub API endpoint
BASE_URL = "https://api.github.com"
headers = {
    "Authorization": f"token {os.environ['GITHUB_TOKEN']}"
}

# Function to fetch users in Basel with over 10 followers
def fetch_users(location="Basel", min_followers=10):
    users_data = []
    page = 1

    while True:
        response = requests.get(
            f"{BASE_URL}/search/users?q=location:{location}+followers:>{min_followers}&page={page}",
            headers=headers
        )
        data = response.json().get('items', [])
        if not data:
            break
        for user in data:
            user_detail = requests.get(user['url'], headers=headers).json()
            users_data.append(user_detail)
        page += 1

    return users_data

# Function to fetch repositories for a given user
def fetch_repositories(username):
    repos_data = []
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}/users/{username}/repos?per_page=100&page={page}", headers=headers)
        data = response.json()
        if not data:
            break
        repos_data.extend(data)
        page += 1

    return repos_data

# Fetch users and repositories
users = fetch_users()
users_list = []
repos_list = []

# Process users and repositories
for user in users:
    # User data for users.csv
    user_data = {
        "login": user.get("login", ""),
        "name": user.get("name", ""),
        "company": user.get("company", "").strip().lstrip('@').upper() if user.get("company") else "",
        "location": user.get("location", ""),
        "email": user.get("email", ""),
        "hireable": user.get("hireable", ""),
        "bio": user.get("bio", ""),
        "public_repos": user.get("public_repos", 0),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "created_at": user.get("created_at", "")
    }
    users_list.append(user_data)

    # Repository data for repositories.csv
    repositories = fetch_repositories(user.get("login"))
    for repo in repositories[:500]:  # Limit to 500 repositories
        repo_data = {
            "login": user.get("login", ""),
            "full_name": repo.get("full_name", ""),
            "created_at": repo.get("created_at", ""),
            "stargazers_count": repo.get("stargazers_count", 0),
            "watchers_count": repo.get("watchers_count", 0),
            "language": repo.get("language", ""),
            "has_projects": repo.get("has_projects", False),
            "has_wiki": repo.get("has_wiki", False),
            "license_name": repo.get("license", {}).get("key", "")
        }
        repos_list.append(repo_data)

# Save data to CSV files
users_df = pd.DataFrame(users_list)
repos_df = pd.DataFrame(repos_list)
users_df.to_csv("users.csv", index=False)
repos_df.to_csv("repositories.csv", index=False)

# Create README.md content
readme_content = """
# GitHub Basel User Data Analysis

### Summary
- **Data Scraping**: Used the GitHub API to scrape users in Basel with over 10 followers and their repositories.
- **Findings**: The most interesting finding was [insert interesting finding based on analysis].
- **Recommendation**: For developers looking to increase followers, [insert recommendation].

### Files
- **users.csv**: Contains user data for GitHub users in Basel.
- **repositories.csv**: Contains repository data for the users in users.csv.

### Setup
1. Clone the repository.
2. Install necessary packages with `pip install pandas requests`.
3. Run the analysis script to get insights.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
"""

# Save README file
with open("README.md", "w") as f:
    f.write(readme_content)

# GitHub repository setup
def create_github_repo(repo_name):
    url = f"{BASE_URL}/user/repos"
    data = {"name": repo_name, "private": False}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Repository created successfully.")
        return response.json()["clone_url"]
    else:
        print("Failed to create repository:", response.json())
        return None

# Push files to the repository
def push_to_github_repo(repo_name):
    from git import Repo
    
    repo_url = create_github_repo(repo_name)
    if not repo_url:
        return
    
    # Initialize a local Git repository and commit files
    repo = Repo.init()
    repo.git.add(all=True)
    repo.index.commit("Initial commit with users.csv, repositories.csv, and README.md")

    # Set remote and push
    origin = repo.create_remote('origin', repo_url)
    origin.push(refspec='main:main')
    print(f"Pushed to {repo_url}")

# Execute functions to create and push to GitHub repo
repo_name = "basel-github-users"
push_to_github_repo(repo_name)
