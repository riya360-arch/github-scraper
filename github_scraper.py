import os
import requests

# Use an environment variable for security (recommended), or set it directly in code
GITHUB_TOKEN = os.getenv("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")  # Replace with your actual token if not using .env
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def search_users_in_basel():
    url = "https://api.github.com/search/users"
    params = {
        "q": "location:Basel followers:>10",
        "per_page": 100  # Max results per page
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()  # Checks for request errors
    
    users_data = response.json().get("items", [])
    return users_data  # Returns a list of users

def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    user_data = response.json()
    return user_data  # Returns detailed information about the user

def get_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    params = {
        "per_page": 100  # Max results per page
    }
    
    all_repos = []
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        
        repos_data = response.json()
        all_repos.extend(repos_data)
        
        # Check if there's a next page
        url = response.links.get("next", {}).get("url")
        if len(all_repos) >= 500:
            break  # Limit to 500 repositories per user
            
    return all_repos  # Returns a list of repositories for the user

import csv

def main():
    # Search for users
    basel_users = search_users_in_basel()
    
    # Prepare CSV files
    with open("users.csv", "w", newline='') as users_file, open("repositories.csv", "w", newline='') as repos_file:
        user_writer = csv.writer(users_file)
        repo_writer = csv.writer(repos_file)
        
        # Write headers
        user_writer.writerow(["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"])
        repo_writer.writerow(["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"])
        
        # Fetch details and repositories for each user
        for user in basel_users:
            username = user["login"]
            user_details = get_user_details(username)
            
            # Write user details to users.csv
            user_writer.writerow([
                user_details.get("login"),
                user_details.get("name", ""),
                user_details.get("company", "").lstrip("@").upper().strip(),
                user_details.get("location", ""),
                user_details.get("email", ""),
                user_details.get("hireable", ""),
                user_details.get("bio", ""),
                user_details.get("public_repos"),
                user_details.get("followers"),
                user_details.get("following"),
                user_details.get("created_at")
            ])
            
            # Fetch repositories and write to repositories.csv
            user_repositories = get_user_repositories(username)
            for repo in user_repositories:
                repo_writer.writerow([
                    username,
                    repo.get("full_name", ""),
                    repo.get("created_at", ""),
                    repo.get("stargazers_count", 0),
                    repo.get("watchers_count", 0),
                    repo.get("language", ""),
                    repo.get("has_projects", False),
                    repo.get("has_wiki", False),
                    repo.get("license", {}).get("key", "")
                ])

if __name__ == "__main__":
    main()

