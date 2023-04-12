from rest_framework.views import APIView
from rest_framework.response import Response

import requests
from bs4 import BeautifulSoup

from student.serializers import StudentSerializer, TechnicalProfileSerializer, WorkExpProfileSerializer
from student.models import Student, TechnicalProfile, WorkExpProfile

# Create your views here.

class StudentView(APIView):
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TechnicalProfileView(APIView):
    def get(self, *args, **kwargs):
        tech_profile = TechnicalProfile.objects.filter(id=self.kwargs['student_id']).first()
        serializer = TechnicalProfileSerializer(tech_profile)
        return Response(serializer.data)
    
    def post(self, request):
        git_username = request.data['git_username']

        dev_details = {}

        # get commits and PRs
        commits_url = "https://github-readme-stats.vercel.app/api?username=" + git_username + "&count_private=true"
        commits_res = requests.get(commits_url)
        commits_soup = BeautifulSoup(commits_res.content, 'html.parser')
        commits_elem = commits_soup.find('desc').text

        substrings = commits_elem.split(', ')
        key_value_pairs = [substring.split(': ') for substring in substrings]
        dev_details = {key.strip(): value.strip() for key, value in key_value_pairs}

        total_commits = dev_details['Total Commits in 2023']
        total_prs = dev_details['Total PRs']

        dev_details['git_username'] = git_username
        dev_details['total_commits'] = total_commits
        dev_details['total_prs'] = total_prs

        del dev_details['Total Stars Earned']
        del dev_details['Total Issues']
        del dev_details['Contributed to (last year)']
        del dev_details['Total PRs']
        del dev_details['Total Commits in 2023']

        # get top langauges
        lang_url = "https://github-readme-stats.vercel.app/api/top-langs/?username=" + git_username
        lang_res = requests.get(lang_url)
        lang_soup = BeautifulSoup(lang_res.content, 'html.parser')
        lang_elem = lang_soup.find_all('g', {'class': 'stagger'})

        top_languages = []

        for lang in lang_elem:
            language = lang.find('text', {'x': '2'}).text
            percentage = lang.find('text', {'x': '215'}).text

            top_languages.append({
                'lang': language,
                'perc': percentage
            })

        dev_details['top_languages'] = top_languages

        # get streak
        streak_url = "https://streak-stats.demolab.com/?user=" + git_username
        streak_res = requests.get(streak_url)
        streak_soup = BeautifulSoup(streak_res.content, 'html.parser')
        streak = streak_soup.find('text', {'style': 'animation: currstreak 0.6s linear forwards'}).text.strip()

        dev_details['current_streak'] = streak

        headers = {
            'Authorization': 'Bearer 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'
        }

        repos_url = "https://api.github.com/users/" + git_username + "/repos"
        repos_res = requests.get(repos_url, headers=headers)
        repos_json = repos_res.json()

        repos = []

        for repo in repos_json:
            name = repo['name']
            language = repo['language']
            stargazers_count = repo['stargazers_count']
            commits_url = repo['commits_url'].replace('{/sha}', '')
            
            commits_response = requests.get(commits_url)
            commits = commits_response.json()
            num_commits = len(commits)
            
            repos.append({
                'name': name,
                'language': language,
                'stars': stargazers_count,
                'num_commits': num_commits
            })


        dev_details['repos'] = repos

        serializer = TechnicalProfileSerializer(data=dev_details)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class WorkExpProfileView(APIView):
    def get(self, *args, **kwargs):
        workexp_profile = WorkExpProfile.objects.filter(id=self.kwargs['student_id']).first()
        serializer = WorkExpProfileSerializer(workexp_profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkExpProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        workexp_profile = WorkExpProfileSerializer.objects.filter(id=self.kwargs['student_id']).first()
        serializer = WorkExpProfileSerializer(
            workexp_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class AllStudentsView(APIView):
    def get(self, request):
        students = Student.objects.all()
        students_serializer = StudentSerializer(
            students, many=True)
        return Response(students_serializer.data)