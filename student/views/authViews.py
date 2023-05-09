from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime

from student.serializers import StudentSerializer
from student.models.studentModels import Student


class LoginView(APIView):
    def get(self, *args, **kwargs):
        student = Student.objects.filter(email=self.kwargs['email']).first()
        if student is None:
            return Response('Email Not Found')
        else:
            serializer = StudentSerializer(student)
            return Response(serializer.data)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        student = Student.objects.filter(email=email).first()

        if student is None:
            raise AuthenticationFailed(
                'Student not found!')

        if not student.check_password(password):
            raise AuthenticationFailed(
                'Incorrect password!')

        payload = {
            'id': student.id,
            'exp': datetime.datetime.now() + datetime.timedelta(days=7),
            'iat': datetime.datetime.now()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        student = Student.objects.filter(id=payload['id']).first()
        lastActive = datetime.datetime.now()
        serializer = StudentSerializer(student,
                                       data={"last_active": lastActive.strftime(
                                           "%a, %d/%m/%y, %H:%M"), "student_token": token},
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # response.set_cookie(key='jwt', value=token, httponly=True)

        return Response(serializer.data)


class CrudUserView(APIView):
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def post(self, request):
        student_email = request.data['email']
        student = Student.objects.filter(email=student_email).first()
        if student is None:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed(
                'Email exists!')

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(
            student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, *args, **kwargs):
        Student.objects.filter(id=self.kwargs['student_id']).delete()
        return Response('Deleted Successfully')


class ForgotPasswordView(APIView):
    def patch(self, request, *args, **kwargs):
        student = Student.objects.filter(email=self.kwargs['email']).first()
        serializer = StudentSerializer(
            student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password Reset Successful')


class AllStudentsView(APIView):
    def get(self, request):
        students = Student.objects.all()
        students_serializer = StudentSerializer(
            students, many=True)
        return Response(students_serializer.data)
