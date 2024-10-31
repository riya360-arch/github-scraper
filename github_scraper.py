import requests
import csv
import os

# GitHub API base URL
GITHUB_API_BASE_URL = "https://api.github.com"

# Function to fetch users based on location and followers
def fetch_users(location, min_followers):
    url = f"{GITHUB_API_BASE_URL}/search/users?q=location:{location}+followers:>{min_followers}"
    headers = {"Authorization": f"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"}  # Replace with your GitHub token
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json().get("items", [])

# Function to fetch repositories for a given user
def fetch_user_repositories(username):
    url = f"{GITHUB_API_BASE_URL}/users/{username}/repos"
    headers = {"Authorization": f"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"}  # Replace with your GitHub token
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to clean and process user data
def clean_company_name(company):
    return company.lstrip("@").strip().upper() if company else ""

def clean_hireable(hireable):
    return hireable if isinstance(hireable, bool) else ""

def clean_bio(bio):
    return bio if bio is not None else ""

# Function to save users to CSV
def save_users_to_csv(users_data):
    headers = ["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"]
    with open("users.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write header row

        for user in users_data:
            company = clean_company_name(user.get("company", ""))
            hireable = clean_hireable(user.get("hireable", None))
            bio = clean_bio(user.get("bio", None))
            writer.writerow([
                user.get("login", ""),
                user.get("name", ""),
                company,
                user.get("location", ""),
                user.get("email", ""),
                hireable,
                bio,
                user.get("public_repos", 0),
                user.get("followers", 0),
                user.get("following", 0),
                user.get("created_at", "")
            ])

# Function to save repositories to CSV
def save_repositories_to_csv(repos_data):
    headers = ["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"]
    with open("repositories.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write header row

        for repo in repos_data:
            # Safely handle the license retrieval
            license_name = ""
            if repo.get("license") is not None:
                license_name = repo["license"].get("key", "")

            writer.writerow([
                repo.get("owner", {}).get("login", ""),
                repo.get("full_name", ""),
                repo.get("created_at", ""),
                repo.get("stargazers_count", 0),
                repo.get("watchers_count", 0),
                repo.get("language", ""),
                repo.get("has_projects", False),
                repo.get("has_wiki", False),
                license_name
            ])


# Main function to orchestrate the data fetching and saving
def main():
    location = "Basel"
    min_followers = 10
    users_data = fetch_users(location, min_followers)

    # Save users data to CSV
    save_users_to_csv(users_data)

    # For each user, fetch their repositories
    for user in users_data:
        username = user['login']
        repos_data = fetch_user_repositories(username)
        save_repositories_to_csv(repos_data)

if __name__ == "__main__":
    main()