from rest_framework import serializers

from news.models import NewsPiece, TechEvent, TechJob

class NewsPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPiece
        fields = '__all__'

class TechEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechEvent
        fields = '__all__'

class TechJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechJob
        fields = '__all__'