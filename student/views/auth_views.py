from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import smtplib
import random

from student.serializers import StudentSerializer
from student.models import Student

class LoginView(APIView):
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
            data={"last_active": lastActive.strftime("%a, %d/%m/%y, %H:%M"), "student_token": token}, 
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # response.set_cookie(key='jwt', value=token, httponly=True)

        return Response(serializer.data)


class UserView(APIView):
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def post(self, request):
        email = request.data['email']
        student = Student.objects.filter(email=email).first()
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
        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, *args, **kwargs):
        Student.objects.filter(id=self.kwargs['student_id']).delete()
        return Response('Deleted Successfully')


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        return Response('Logged Out')
    
    
class ForgotPasswordView(APIView):
    def post(self, request):
        receiver_email = request.data['email']
        student = Student.objects.filter(email=receiver_email).first()

        if student is None:
            return Response('email not found')
        else: 
            otp_holder = ''
            for i in range(6):
                otp_holder += str(random.randint(0, 9))
            otp = int(otp_holder)

            sender_email = "your_email@example.com"
            sender_password = "your_email_password"
            
            message = f"Hello there!. Your one-time password is: {otp}. Note that the OTP is only active for 10 minutes!"
            
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, receiver_email, message)
            
            serializer = StudentSerializer(student,
                                           data={"reset_otp": otp, "reset_time":  datetime.datetime.now()}, 
                                            partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response('otp sent successfully')


class ResetOTPView(APIView):
    def post(self, request):
        student_email = request.data['email']
        student_otp = request.data['otp']

        student = Student.objects.filter(email=student_email).first()
        reset_otp = student.getOTP()
        reset_time = student.getOTPTime()

        time_diff = datetime.datetime.now() - reset_time

        if(time_diff < 10):
            if(reset_otp == student_otp):
                return Response('Security Check Passed!')
            else:
                return Response('Security Check Failed!')
        else:
            return Response('OTP is inactive!')
    
# TODO : Verify email on account creation
# TODO : Create elira email account
# TODO : Test forgot password functionality