from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentSerializer
from .models import Student

class AllUsersView(APIView):
    def get(self, request):
        users = Student.objects.all()
        users_serializer = StudentSerializer(
            users, many=True)
        return Response(users_serializer.data)
