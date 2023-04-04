from rest_framework.views import APIView
from rest_framework.response import Response

from news.serializers import NewsPieceSerializer
from news.models import NewsPiece

# ---------------------- NewsPiece Views ------------------------------------
class NewsPieceByTagView(APIView):
    def get(self, request):
        tags = request.GET.get('tag')

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