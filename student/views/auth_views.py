from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
import jwt
import datetime
import requests

from student.serializers import StudentSerializer
from student.models import Student

ABSTARCT_API_KEY = '314ceea02b4b4c46afa1e64279bcbde2'
ABSTARCT_API_URL = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + ABSTARCT_API_KEY


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
                                       data={"last_active": lastActive.strftime(
                                           "%a, %d/%m/%y, %H:%M"), "student_token": token},
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
        student_email = request.data['email']
        student = Student.objects.filter(email=student_email).first()
        if student is None:
            # check to confirm email is valid
            abstractAPI_res = requests.get(
                ABSTARCT_API_URL + "&email=" + student_email)
            is_valid_email = is_valid(abstractAPI_res.content)

            if is_valid_email:
                # send verification code
                unique_code = get_random_string(
                    length=6, allowed_chars='0123456789')
                send_mail(
                    subject="One Last Step: Let's get you verified",
                    message=f'''
                        Welcome Aboard!
                        Thank you for signing up for Elira! Here's you're one time passcode:

                        {unique_code}

                        Here's to becoming a stellar graduate! We look forward to serving you!

                        If you did not sign up for Elira, please ignore this email.

                        Best regards,
                        Elira Team
                            ''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student_email])

                # create user account
                student_data = {"email": student_email,
                                "first_name": request.data['first_name'],    "last_name": request.data['last_name'],
                                "school": request.data['school'],
                                "course": request.data['course'],
                                "current_sem": request.data['current_sem'],
                                "verify_otp": int(unique_code)},
                serializer = StudentSerializer(data=student_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            else:
                raise AuthenticationFailed(
                    'Invalid Email!')
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

# Email Validator function
def is_valid(data):
    if data.is_valid_format.value and data.is_mx_found and data.is_smtp_valid:
        if not data.is_catchall_email and not data.is_role_email and not data.is_free_email:
            return True
        else:
            return False
    else:
        return False


class VerifyUserView(APIView):
    def get(self, *args, **kwargs):
        student = Student.objects.filter(id=self.kwargs['student_id']).first()
        isVerified = student.getIsVerified()
        return Response(str(isVerified))

    def post(self, request):
        verify_otp = request.data['verify_otp']
        student = Student.objects.filter(id=request.data['student_id']).first()
        std_verify_code = student.getVerifyCode()
        if std_verify_code == verify_otp:
            serializer = StudentSerializer(student, data={"isVerified": True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response('Verified!')
        else:
            Response('Wrong Code!')

class ForgotPasswordView(APIView):
    def post(self, request):
        student_email = request.data['email']
        student = Student.objects.filter(email=student_email).first()

        if student is None:
            return Response('email not found')
        else:
            unique_code = get_random_string(
                    length=6, allowed_chars='0123456789')
            send_mail(
                    subject="Forgot your password? Happens to the best of us",
                    message=f'''
                        Hello there! Here's you're reset passcode:

                        {unique_code}

                        Please note that the code is active for only 5 minutes!

                        Best regards,
                        Elira Team
                            ''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[student_email])

            serializer = StudentSerializer(student,
                                           data={
                                               "reset_otp": int(unique_code), "reset_expiry":  datetime.datetime.now() + datetime.timedelta(minutes=10)},
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
        reset_expiry = student.getOTPTime()

        time_diff = datetime.datetime.now() - reset_expiry

        if (time_diff < 10):
            if (reset_otp == student_otp):
                return Response('Security Check Passed!')
            else:
                return Response('Security Check Failed!')
        else:
            return Response('OTP is inactive!')


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        return Response('Logged Out')