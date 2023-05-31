from rest_framework.views import APIView
from rest_framework.response import Response

from progress.models import AppData, ProjectIdea
from progress.serializers import AppDataSerializer, ProjectIdeaSerializer


class ProjectIdeasView(APIView):    # pass specialisation
    def get(self, *args, **kwargs):
        ideaIndexObj = AppData.objects.filter(name="projetIdeaIndex").first()
        ideaIndex = ideaIndexObj.currentIndex
        beginnerIdeas = ProjectIdea.objects.filter(specialisation=self.kwargs['specialisation'], level="B")
        interIdeas = ProjectIdea.objects.filter(specialisation=self.kwargs['specialisation'], level="I")
        advIdeas = ProjectIdea.objects.filter(specialisation=self.kwargs['specialisation'], level="A")

        # get today's 3 ideas
        todaysIdeas = []
        todaysIdeas.append(ProjectIdeaSerializer(data=beginnerIdeas[ideaIndex]).data)
        todaysIdeas.append(ProjectIdeaSerializer(data=interIdeas[ideaIndex]).data)
        todaysIdeas.append(ProjectIdeaSerializer(data=advIdeas[ideaIndex]).data)

        # update index for tomorrow
        appDataSer = AppDataSerializer(data={"current_value": ideaIndex + 1}, partial=True)
        appDataSer.is_valid(raise_exception=True)
        appDataSer.save()

        return Response({"ideas" : todaysIdeas})

    def post(self, request):
        serializer = ProjectIdeaSerializer(data=request.data['projectIdeas'], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('All Project Ideas Uploaded Successfully')

class AllProjectIdeasView(APIView):    
    def get(self, *args, **kwargs):
        ideas = ProjectIdea.objects.all()
        ideas_serializer = ProjectIdeaSerializer(
            ideas, many=True)
        return Response(ideas_serializer.data)
    
    
class AppDataView(APIView):
    def post(self, request):
        serializer = AppDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('App Data Added Successfully')