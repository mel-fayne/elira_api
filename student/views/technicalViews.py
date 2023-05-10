import requests
from bs4 import BeautifulSoup

from rest_framework.views import APIView
from rest_framework.response import Response

from student.models.technicalModels import TechnicalProfile
from student.serializers import TechnicalProfileSerializer

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

LANGUAGES = [
    ('c', 'C'),
    ('cmake', 'CMake'),
    ('cPlusPlus', 'C++'),
    ('java', 'Java'),
    ('javascript', 'JavaScript'),
    ('python', 'Python'),
    ('r', 'R'),
    ('jupyter', 'Jupyter Notebook'),
    ('dart', 'Dart'),
    ('kotlin', 'Kotlin'),
    ('go', 'Go'),
    ('swift', 'Swift'),
    ('cSharp', 'C#'),
    ('aspNet', 'ASP.NET'),
    ('typescript', 'Typescript'),
    ('php', 'PHP'),
    ('objective_c', 'Objective-C'),
    ('ruby', 'Ruby'),
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('scss', 'SCSS'),
    ('sql', 'SQL'),
    ('rust', 'Rust')]


class TechnicalProfileView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        accessRes = requests.get(
            'https://api.github.com/rate_limit', headers=HEADERS)
        accessData = accessRes.json()
        accessRem = accessData['resources']['core']['remaining']

        if accessRem > 0:
            tech_profile = TechnicalProfile.objects.filter(
                student_id=self.kwargs['student_id']).first()
            git_name = tech_profile.gitName
            devData = getGitData(git_name)
            devData['git_username'] = git_name

            serializer = TechnicalProfileSerializer(
                tech_profile, data=devData, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            tech_profile = TechnicalProfile.objects.filter(
                student_id=self.kwargs['student_id']).first()
            serializer = TechnicalProfileSerializer(tech_profile)
            return Response('Github API Access Limit Reached')

    def post(self, request):    # pass git_username & student_id
        accessRes = requests.get(
            'https://api.github.com/rate_limit', headers=HEADERS)
        accessData = accessRes.json()
        accessRem = accessData['resources']['core']['remaining']

        if accessRem > 0:
            git_name = request.data['git_username']
            devData = getGitData(git_name)

            if devData == {}:
                return Response('Github User Not Found')

            else:
                devData['git_username'] = git_name
                devData['student_id'] = request.data['student_id']
                print(devData)
                serializer = TechnicalProfileSerializer(data=devData)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else:
            return Response('Github API Access Limit Reached')

    def patch(self, request, *args, **kwargs):    # pass new git_username & student_id
        accessRes = requests.get(
            'https://api.github.com/rate_limit', headers=HEADERS)
        accessData = accessRes.json()
        accessRem = accessData['resources']['core']['remaining']

        if accessRem > 0:
            tech_profile = TechnicalProfile.objects.filter(
                student_id=self.kwargs['student_id']).first()
            git_name = request.data['git_username']
            devData = getGitData(git_name)

            if devData == {}:
                return Response('Github User Not Found')

            else:
                devData['git_username'] = git_name
                serializer = TechnicalProfileSerializer(
                    tech_profile, data=devData, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else:
            return Response('Github API Access Limit Reached')


def getGitData(git_name):
    devData = {}

    # get commits and PRs
    commits_url = "https://github-readme-stats.vercel.app/api?username=" + \
        git_name + "&count_private=true"
    commits_res = requests.get(commits_url, headers=HEADERS)
    commits_soup = BeautifulSoup(commits_res.content, 'html.parser')
    stars = commits_soup.find('text', {'data-testid': 'stars'})

    if stars:
        devData['total_stars'] = stars.text
        commits = commits_soup.find(
            'text', {'data-testid': 'commits'}).text
        if 'k' in commits:
            commits = commits.replace("k", "").replace(".", "")
            commits = int(commits) * 1000
        devData['total_commits'] = commits
        devData['total_prs'] = commits_soup.find(
            'text', {'data-testid': 'prs'}).text
        devData['total_issues'] = commits_soup.find(
            'text', {'data-testid': 'issues'}).text
        devData['total_contribs'] = commits_soup.find(
            'text', {'data-testid': 'contribs'}).text

        # get top langauges
        lang_url = "https://github-readme-stats.vercel.app/api/top-langs/?username=" + git_name
        lang_res = requests.get(lang_url, headers=HEADERS)
        lang_soup = BeautifulSoup(lang_res.content, 'html.parser')
        lang_elem = lang_soup.find_all('g', {'class': 'stagger'})

        topFive = []
        for lang in lang_elem:
            language = lang.find('text', {'x': '2'}).text
            percentage = lang.find('text', {'x': '215'}).text
            topFive.append(language)
            for langTuple in LANGUAGES: # fill the top 5 languages
                if langTuple[1] == language:
                    percentage = percentage.replace("%", "")
                    devData[langTuple[0]] = float(percentage)


        for langTuple in LANGUAGES:     # make the others zero
            if langTuple[1] not in topFive:
                devData[langTuple[0]] = 0


        # get streak
        streak_url = "https://streak-stats.demolab.com/?user=" + git_name
        streak_res = requests.get(streak_url, headers=HEADERS)
        streak_soup = BeautifulSoup(streak_res.content, 'html.parser')
        streak = streak_soup.find(
            'text', {'style': 'animation: currstreak 0.6s linear forwards'}).text.strip()
        devData['current_streak'] = streak

    else:
        devData = {}

    return devData

