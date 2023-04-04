from rest_framework.views import APIView
from rest_framework.response import Response

from student.serializers import StudentSerializer
from student.models import Student

# Create your views here.
class AllStudentsView(APIView):
    def get(self, request):
        students = Student.objects.all()
        students_serializer = StudentSerializer(
            students, many=True)
        return Response(students_serializer.data)