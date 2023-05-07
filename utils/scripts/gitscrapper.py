import requests
from bs4 import BeautifulSoup

print('***************** Starting Git Status Update *****************')

# profiles = TechnicalProfile.objects.all()
profiles = ['hgh7789']

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

for profile in profiles:
    dev_details = {}
    git_name = profile

    # get commits and PRs
    commits_url = "https://github-readme-stats.vercel.app/api?username=" + \
        git_name + "&count_private=true"
    commits_res = requests.get(commits_url, headers=HEADERS)
    commits_soup = BeautifulSoup(commits_res.content, 'html.parser')

    stars = commits_soup.find('text', {'data-testid': 'stars'})
    if stars:
        dev_details['stars'] = stars.text
    else:
        dev_details['stars'] = 0
    commits = commits_soup.find('text', {'data-testid': 'commits'}).text
    prs = commits_soup.find('text', {'data-testid': 'prs'}).text
    issues = commits_soup.find('text', {'data-testid': 'issues'}).text
    contribs = commits_soup.find('text', {'data-testid': 'contribs'}).text

    dev_details['total_commits'] = commits
    dev_details['total_prs'] = prs
    dev_details['total_stars'] = stars
    dev_details['total_issues'] = issues

    print(dev_details)

#     # get top langauges
#     lang_url = "https://github-readme-stats.vercel.app/api/top-langs/?username=" + git_name
#     lang_res = requests.get(lang_url, headers=HEADERS)
#     lang_soup = BeautifulSoup(lang_res.content, 'html.parser')
#     lang_elem = lang_soup.find_all('g', {'class': 'stagger'})

#     languages = []

#     for lang in lang_elem:
#         language = lang.find('text', {'x': '2'}).text
#         percentage = lang.find('text', {'x': '215'}).text

#         languages.append({
#             'lang': language,
#             'perc': percentage
#         })

#     dev_details['top_languages'] = languages

#     # get streak
#     streak_url = "https://streak-stats.demolab.com/?user=" + git_name
#     streak_res = requests.get(streak_url, headers=HEADERS)
#     streak_soup = BeautifulSoup(streak_res.content, 'html.parser')
#     streak = streak_soup.find(
#         'text', {'style': 'animation: currstreak 0.6s linear forwards'}).text.strip()

#     dev_details['streak'] = streak
    
#     print(dev_details)

#     # serializer = TechnicalProfileSerializer(profile, data=dev_details, partial=True)
#     # serializer.is_valid(raise_exception=True)
#     # serializer.save()


# print('***************** Finished Git Status Update *****************')

# response = requests.get('https://api.github.com/rate_limit', headers=HEADERS)
# data = response.json()

# limit = data['resources']['core']['limit']
# remaining = data['resources']['core']['remaining']
# reset_time = data['resources']['core']['reset']

# print(f"Current access limit: {limit}")
# print(f"Remaining requests: {remaining}")
# print(f"Reset time: {reset_time}")

   

