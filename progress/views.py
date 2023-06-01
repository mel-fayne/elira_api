from rest_framework.views import APIView
from rest_framework.response import Response

from progress.models import AppData, ProjectIdea, StudentProject
from progress.serializers import AppDataSerializer, ProjectIdeaSerializer, StudentProjectSerializer
from student.models.studentModels import Student


class ProjectIdeasView(APIView):    # pass specialisation
    def get(self, *args, **kwargs):
        ideaIndexObj = AppData.objects.filter(name="projetIdeaIndex").first()
        ideaIndex = ideaIndexObj.currentIndex
        beginnerIdeas = ProjectIdea.objects.filter(
            specialisation=self.kwargs['specialisation'], level="B")
        interIdeas = ProjectIdea.objects.filter(
            specialisation=self.kwargs['specialisation'], level="I")
        advIdeas = ProjectIdea.objects.filter(
            specialisation=self.kwargs['specialisation'], level="A")

        # get today's 3 ideas
        todaysIdeas = []
        todaysIdeas.append(ProjectIdeaSerializer(
            beginnerIdeas[ideaIndex]).data)
        todaysIdeas.append(ProjectIdeaSerializer(interIdeas[ideaIndex]).data)
        todaysIdeas.append(ProjectIdeaSerializer(advIdeas[ideaIndex]).data)

        return Response({"ideas": todaysIdeas})

    def post(self, request):
        serializer = ProjectIdeaSerializer(
            data=request.data['projectIdeas'], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('All Project Ideas Uploaded Successfully')


class StudentProjectView(APIView):          # pass studentId
    def get(self, *args, **kwargs):
        ongoingPrjs = StudentProject.objects.filter(
            student_id=self.kwargs['student_id'], status="O")
        completedPrjs = StudentProject.objects.filter(
            student_id=self.kwargs['student_id'], status="C")
        studentProjects = {}
        studentProjects['ongoing'] = StudentProjectSerializer(
            ongoingPrjs, many=True).data
        studentProjects['completed'] = StudentProjectSerializer(
            completedPrjs, many=True).data

        wishList = Student.objects.filter(
            id=self.kwargs['student_id']).first().projectWishList
        projectWishList = []
        for id in wishList:
            ideaSer = ProjectIdeaSerializer(ProjectIdea.objects.filter(id=id).first())
            projectWishList.append(ideaSer.data)
        studentProjects['projectWishList'] = projectWishList

        return Response(studentProjects)

    def post(self, request):
        serializer = StudentProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):    # pass project_id
        projIdea = StudentProject.objects.filter(id=self.kwargs['project_id']).first()
        serializer = StudentProjectSerializer(projIdea, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, *args, **kwargs):      # pass project_id
        StudentProject.objects.filter(id=self.kwargs['project_id']).first().delete()
        return Response('Deleted Successfully')


class StudentIdeaWishListView(APIView):    # pass studentId
    def get(self, *args, **kwargs):
        wishList = Student.objects.filter(
            id=self.kwargs['student_id']).first().projectWishList
        projectWishList = []
        for id in wishList:
            ideaSer = ProjectIdeaSerializer(ProjectIdea.objects.filter(id=id).first())
            projectWishList.append(ideaSer.data)
        return Response({"ideas": projectWishList})


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
