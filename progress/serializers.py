from rest_framework import serializers

from progress.models import AppData, ProjectIdea

class ProjectIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIdea
        fields = '__all__'

class AppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppData
        fields = '__all__'