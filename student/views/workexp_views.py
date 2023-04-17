from rest_framework.views import APIView
from rest_framework.response import Response

from student.serializers import WorkExpProfileSerializer
from student.models import WorkExpProfile


class WorkExpProfileView(APIView):
    def get(self, *args, **kwargs):
        workexp_profile = WorkExpProfile.objects.filter(id=self.kwargs['student_id']).first()
        serializer = WorkExpProfileSerializer(workexp_profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkExpProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        workexp_profile = WorkExpProfileSerializer.objects.filter(id=self.kwargs['student_id']).first()
        serializer = WorkExpProfileSerializer(
            workexp_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)