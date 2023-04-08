from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime, timedelta
from news.serializers import NewsPieceSerializer, TechEventSerializer, TechJobSerializer
from news.models import NewsPiece, TechEvent, TechJob

# ---------------------- NewsPiece Views ------------------------------------


class NewsPiecesByTagView(APIView):
    def get(self, request):
        tags = request.GET.get('tags')

        if tags:
            tag_list = tags.split(',')
            news_pieces = NewsPiece.objects.filter(tags__in=tag_list)
            news_serializer = NewsPieceSerializer(news_pieces, many=True)
            return Response(news_serializer.data)
        else:
            return Response('no news found')


class AllNewsPiecesView(APIView):
    def get(self):
        news = NewsPiece.objects.all().order_by('date_created')
        news_serializer = NewsPieceSerializer(news, many=True)
        return Response(news_serializer.data)

# ---------------------- TechEvent Views ------------------------------------


class TechEventsByDateView(APIView):
    def get(self, request):
        period = int(request.GET.get('period'))
        lastDate = datetime.date.today() - timedelta(days=period)
        events = TechEvent.objects.filter(date__mt=lastDate)
        events_serializer = TechEventSerializer(events, many=True)
        return Response(events_serializer.data)


class AllTechEventsView(APIView):
    def get(self):
        events = TechEvent.objects.all().order_by('date')
        events_serializer = TechEventSerializer(events, many=True)
        return Response(events_serializer.data)

# ---------------------- TechJobs Views ------------------------------------


class TechJobsByAreaView(APIView):
    def get(self, request):
        areas = request.GET.get('areas')

        if jobs_serializer:
            area_list = areas.split(',')
            jobs = NewsPiece.objects.filter(areas__in=area_list)
            jobs_serializer = TechJobSerializer(jobs, many=True)
            return Response(jobs_serializer.data)
        else:
            return Response('no jobs found')


class AllTechJobsView(APIView):
    def get(self):
        jobs = TechJob.objects.all().order_by('posted')
        jobs_serializer = TechJobSerializer(jobs, many=True)
        return Response(jobs_serializer.data)
