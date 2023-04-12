from rest_framework.views import APIView
from rest_framework.response import Response

from student.serializers import StudentSerializer, TechnicalProfileSerializer
from student.models import Student, TechnicalProfile

# Create your views here.

class StudentView(APIView):
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TechnicalProfileView(APIView):
    def get(self, *args, **kwargs):
        tech_profile = TechnicalProfile.objects.filter(id=self.kwargs['student_id']).first()

        # TODO: check for consistency in fields
        profile_data = {}
        
        serializer = TechnicalProfileSerializer(tech_profile, data=profile_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tech_profile = TechnicalProfile.objects.filter(id=self.kwargs['student_id']).first()
        serializer = TechnicalProfileSerializer(tech_profile)
        return Response(serializer.data)
    
    def post(self, request):

        # TODO: populate fields
        # TODO: calculate technical score
        # TODO: get specialisation rank

        serializer = TechnicalProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class AllStudentsView(APIView):
    def get(self, request):
        students = Student.objects.all()
        students_serializer = StudentSerializer(
            students, many=True)
        return Response(students_serializer.data)