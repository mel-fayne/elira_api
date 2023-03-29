from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import StudentSerializer
from .models import Student
import jwt
import datetime

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Student.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(
                'User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed(
                'Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=48),
            'iat': datetime.datetime.now()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        user = Student.objects.filter(id=payload['id']).first()
        lastActive = datetime.datetime.now()
        serializer = StudentSerializer(user, 
            data={"last_active": lastActive.strftime("%a, %d/%m/%y, %H:%M"), "user_token": token}, 
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # response.set_cookie(key='jwt', value=token, httponly=True)

        return Response(serializer.data)


class UserView(APIView):
    def get(self, *args, **kwargs):
        user = Student.objects.filter(id=self.kwargs['user_id']).first()
        serializer = StudentSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        email = request.data['email']
        user = Student.objects.filter(email=email).first()
        if user is None:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            raise AuthenticationFailed(
                'Email Exists')

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = Student.objects.filter(id=self.kwargs['user_id']).first()
        serializer = StudentSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, *args, **kwargs):
        Student.objects.filter(id=self.kwargs['user_id']).delete()
        return Response('Deleted Successfully')

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class ResetPasswordView(APIView):
    def post(self, request):
        user = Student.objects.filter(reset_key=request.data['reset_key']).first()
        if(user == None):
            data = {}
        else:
            data = {
                'user_id': user.getId(),
                'name': user.getName()
            }
        return Response(data)