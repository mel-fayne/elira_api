from rest_framework import serializers

from progress.models import AppData, ProjectIdea, SpecRoadmap, StudentProject

class ProjectIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIdea
        fields = '__all__'

class StudentProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProject
        fields = '__all__'


class SpecRoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecRoadmap
        fields = '__all__'

class AppDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppData
        fields = '__all__'