from rest_framework import serializers

from news.models import NewsPiece, NewsGroup

class NewsPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPiece
        fields = '__all__'


class NewsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsGroup
        fields = '__all__'