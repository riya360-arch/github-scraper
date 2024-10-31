# github-scraper
- This script scrapes GitHub users in Basel with over 10 followers and fetches their public repository data.
- After analyzing the data, I found that a significant number of users specialize in JavaScript and Python.
- Developers should optimize for popular languages and explore repositories with high follower counts for networking opportunities.

## Project Overview
This project uses the GitHub API to scrape data about users in Basel with more than 10 followers and their repositories. The data is stored in `users.csv` and `repositories.csv`, making it easy for analysis and review.

## Files in This Repository
- **users.csv**: Contains information about each user, such as login, name, company, location, and bio.
- **repositories.csv**: Contains information about each repository, including name, language, star count, and more.
- **github_scraper.py**: The script that scrapes data from GitHub using the GitHub API and saves it to CSV files.