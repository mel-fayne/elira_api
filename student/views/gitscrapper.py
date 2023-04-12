import requests
import os
import sys
import django
from bs4 import BeautifulSoup

# Add the project directory to the Python path
project_dir = '/home/mel/Desktop/code-lab/api/elira_api'
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elira_api.settings')
django.setup()

from student.models import TechnicalProfile
from student.serializers import TechnicalProfileSerializer

print('***************** Starting Git Status Update *****************')

profiles = TechnicalProfile.objects.all()

for profile in profiles:
    dev_details = {}
    git_name  = profile.getGitName()

    # get commits and PRs
    commits_url = "https://github-readme-stats.vercel.app/api?username=" + git_name + "&count_private=true"
    commits_res = requests.get(commits_url)
    commits_soup = BeautifulSoup(commits_res.content, 'html.parser')
    commits_elem = commits_soup.find('desc').text

    substrings = commits_elem.split(', ')
    key_value_pairs = [substring.split(': ') for substring in substrings]
    dev_details = {key.strip(): value.strip() for key, value in key_value_pairs}

    total_commits = dev_details['Total Commits in 2023']
    total_prs = dev_details['Total PRs']

    del dev_details['Total Stars Earned']
    del dev_details['Total Issues']
    del dev_details['Contributed to (last year)']
    del dev_details['Total PRs']
    del dev_details['Total Commits in 2023']

    # get top langauges
    lang_url = "https://github-readme-stats.vercel.app/api/top-langs/?username=" + git_name
    lang_res = requests.get(lang_url)
    lang_soup = BeautifulSoup(lang_res.content, 'html.parser')
    lang_elem = lang_soup.find_all('g', {'class': 'stagger'})

    languages = []

    for lang in lang_elem:
        language = lang.find('text', {'x': '2'}).text
        percentage = lang.find('text', {'x': '215'}).text

        languages.append({
            'lang': language,
            'perc': percentage
        })

    dev_details['top_languages'] = languages

    # get streak
    streak_url = "https://streak-stats.demolab.com/?user=" + git_name
    streak_res = requests.get(streak_url)
    streak_soup = BeautifulSoup(streak_res.content, 'html.parser')
    streak = streak_soup.find('text', {'style': 'animation: currstreak 0.6s linear forwards'}).text.strip()

    dev_details['streak'] = streak

    headers = {
        'Authorization': 'Bearer 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'
    }

    repos_url = "https://api.github.com/users/" + git_name + "/repos"
    repos_res = requests.get(repos_url, headers=headers)
    repos = repos_res.json()

    repo_details = []

    for repo in repos:
        name = repo['name']
        language = repo['language']
        stargazers_count = repo['stargazers_count']
        commits_url = repo['commits_url'].replace('{/sha}', '')
        
        commits_response = requests.get(commits_url)
        commits = commits_response.json()
        num_commits = len(commits)
        
        repo_details.append({
            'name': name,
            'language': language,
            'stars': stargazers_count,
            'num_commits': num_commits
        })


    dev_details['repo_details'] = repo_details

    serializer = TechnicalProfileSerializer(profile, data=dev_details, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


print('***************** Finished Git Status Update *****************')

response = requests.get('https://api.github.com/rate_limit', headers=headers)
data = response.json()

limit = data['resources']['core']['limit']
remaining = data['resources']['core']['remaining']
reset_time = data['resources']['core']['reset']

print(f"Current access limit: {limit}")
print(f"Remaining requests: {remaining}")
print(f"Reset time: {reset_time}")