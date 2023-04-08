from rest_framework import serializers

from news.models import NewsPiece, NewsGroup, TechEvent, TechJob

class NewsPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPiece
        fields = '__all__'


class NewsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsGroup
        fields = '__all__'

class TechEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechEvent
        fields = '__all__'

class TechJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechJob
        fields = '__all__'