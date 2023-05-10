import datetime
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

from news.serializers import NewsPieceSerializer, TechEventSerializer, TechJobSerializer
from news.models import NewsPiece, TechEvent, TechJob
from student.models.studentModels import Student

NEWS_TAGS = {
    'AI': ['AI', 'Data Science'],
    'CS': ['Cybersecurity'],
    'DA': ['Databases'],
    'GD': ['Design', 'Gaming'],
    'HO': ['Internet of Things', 'OS'],
    'IS': ['Mobile Dev', 'Web Dev', 'Databases'],
    'NC': ['Networking', 'Blockchain', 'Cloud Computing'],
    'SD': ['Mobile Dev', 'DevOps', 'Web Dev', 'Programming']
}

JOB_TAGS = {
    'AI': ['Data & AI'],
    'CS': ['Cyber Security'],
    'DA': ['Database'],
    'GD': ['Design'],
    'HO': ['Software'],
    'IS': ['Mobile Dev', 'Web Dev', 'Databases'],
    'NC': ['Networking & Cloud'],
    'SD': ['Developer', 'Software', 'Mobile Dev',  'Web Dev',]
}


class NewsPiecesByTagView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        student_tags = NEWS_TAGS[student.studentSpec]
        news_pieces = NewsPiece.objects.all()

        newsData = {}
        specNews = []
        otherNews = []
        for news in news_pieces:
            for tag in student_tags:
                if tag in news.newsTags:
                    specNews.append(news)
                    break
                else:
                    pass

            if news not in specNews:
                otherNews.append(news)

        news_serializer = NewsPieceSerializer(specNews, many=True)
        newsData['studentNews'] = news_serializer.data
        news_serializer = NewsPieceSerializer(otherNews, many=True)
        newsData['otherNews'] = news_serializer.data

        return Response(newsData)


class TechEventsByDateView(APIView):    # pass period in days
    def get(self, *args, **kwargs):
        period = self.kwargs['period']
        lastDate = datetime.date.today() - timedelta(days=period)
        eventsData = {}

        events = TechEvent.objects.filter(date__gt=lastDate).order_by('date')
        events_serializer = TechEventSerializer(events, many=True)
        eventsData['upcomingEvents'] = events_serializer.data

        events = TechEvent.objects.exclude(date__gt=lastDate).order_by('date')
        events_serializer = TechEventSerializer(events, many=True)
        eventsData['laterEvents'] = events_serializer.data

        return Response(eventsData)


class TechJobsByAreaView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        student_tags = JOB_TAGS[student.studentSpec]
        jobs = TechJob.objects.all()

        jobsData = {}
        specJobs = []
        otherJobs = []
        for job in jobs:
            for tag in student_tags:
                if tag in job.jobAreas:
                    specJobs.append(job)
                    break
                else:
                    pass

            if job not in specJobs:
                otherJobs.append(job)

        jobs_serializer = TechJobSerializer(specJobs, many=True)
        jobsData['studentJobs'] = jobs_serializer.data
        jobs_serializer = TechJobSerializer(otherJobs, many=True)
        jobsData['otherJobs'] = jobs_serializer.data

        return Response(jobsData)
