from rest_framework.views import APIView
from rest_framework.response import Response

from student.models.softSkillsModels import SoftSkillProfile, SoftSkill
from student.serializers import SoftSkillProfileSerializer, SoftSkillSerializer


class SoftSkillProfileView(APIView):
    def get(self, *args, **kwargs):     # pass studentId
        ss_data = {}
        softskill_profile = SoftSkillProfile.objects.filter(student_id=self.kwargs['student_id']).first()
        ssp_serializer = SoftSkillProfileSerializer(softskill_profile)
        ss_data['ss_profile'] = ssp_serializer.data

        ssProfId = softskill_profile.ssProfileId

        skills = SoftSkill.objects.filter(ss_profile=ssProfId)
        ss_serializer = SoftSkillSerializer(skills, many=True)
        ss_data['skills'] = ss_serializer.data

        return Response(ss_data)

    def post(self, request):    # pass studentId
        # create ss_profile
        ssp_serializer = SoftSkillProfileSerializer(data={'student_id': request.data['student_id']})
        ssp_serializer.is_valid(raise_exception=True)
        ssp_serializer.save()

        # create skills for this ss_profile
        ss_profile = SoftSkillProfile.objects.filter(student_id=request.data['student_id']).first()
        skills = [
                'Teamwork',
                'Adaptability',
                'Problem Solving',
                'Critical Thinking',
                'Communication',
                'Interpersonal Skills',
                'Leadership',
                'Responsibility'
            ]
        for name in skills:
            skill_data = {}
            skill_data['name'] = name
            skill_data['score'] = 0
            skill_data['ss_profile'] = ss_profile.ssProfileId

            ss_serializer = SoftSkillSerializer(data=skill_data)
            ss_serializer.is_valid(raise_exception=True)
            ss_serializer.save()

        ssp_serializer = SoftSkillProfileSerializer(ss_profile, data={'soft_skill_score': 0}, partial=True)
        ssp_serializer.is_valid(raise_exception=True)
        ssp_serializer.save()

        return Response(ssp_serializer.data)

    def patch(self, request, *args, **kwargs):      # pass studentId & softSkill data
        ss_profile = SoftSkillProfile.objects.filter(student_id=self.kwargs['student_id']).first()

        skill = SoftSkill.objects.filter(id=request.data['id']).first()
        ss_serializer = SoftSkillSerializer(skill, data=request.data, partial=True)
        ss_serializer.is_valid(raise_exception=True)
        ss_serializer.save()

        # compute ss score
        avg = 0.0
        skills = SoftSkill.objects.filter(ss_profile=ss_profile.ssProfileId)
        for skill in skills:
            sc = (skill.ssScore * 12.5) / 100
            avg = avg + sc

        profileData = {}
        profileData['soft_skill_score'] = avg

        serializer = SoftSkillProfileSerializer(
            ss_profile, data=profileData, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
