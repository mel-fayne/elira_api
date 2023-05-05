# from rest_framework.views import APIView
# from rest_framework.response import Response

# from student.models import SoftSkill, SoftSkillProfile, Student
# from student.serializers import SoftSkillProfileSerializer, SoftSkillSerializer


# class SoftSkillProfileView(APIView):
#     def get(self, *args, **kwargs):
#         ss_data = {}
#         softskill_profile = SoftSkillProfile.objects.filter(id=self.kwargs['student_id']).first()
#         ssp_serializer = SoftSkillProfileSerializer(softskill_profile)
#         ss_data['ss_profile'] = ssp_serializer.data

#         skills = SoftSkill.objects.filter(id=softskill_profile.getId())
#         ss_serializer = SoftSkillSerializer(skills, many=True)
#         ss_data['skills'] = ss_serializer.data

#         return Response(ss_data)

#     def post(self, request):
#         student_id = request.data['student_id']
#         student = Student.objects.filter(id=student_id).first()

#         # create ss_profile  
#         ssp_serializer = SoftSkillProfileSerializer(data={'student_id': student})
#         ssp_serializer.is_valid(raise_exception=True)
#         ssp_serializer.save()

#         # create skills for this ss_profile 
#         ss_profile = SoftSkillProfile.objects.filter(id=student).first()
#         scores = []
#         for skill in request.data['skills']:
#             skill_data = {}

#             skill_data['name'] = skill['name']
#             skill_data['score'] = skill['score']
#             scores.append(skill['score']) # to be used to comppute ss score
#             skill_data['ss_profile'] = ss_profile

#             ss_serializer = SoftSkillSerializer(data=skill_data)
#             ss_serializer.is_valid(raise_exception=True)
#             ss_serializer.save()
        
#         # compute ss score
#         avg = 0.0
#         for score in scores:
#             sc = (score * 10) / 100
#             avg = avg + sc
        
#         ssp_serializer = SoftSkillProfileSerializer(ss_profile, data={'soft_skill_score': avg}, partial=True)
#         ssp_serializer.is_valid(raise_exception=True)
#         ssp_serializer.save()
#         return Response(ss_serializer.data)

#     def patch(self, request, *args, **kwargs):
#         ss_profile = SoftSkillProfileSerializer.objects.filter(id=self.kwargs['student_id']).first()
       
#         skills = SoftSkill.objects.filter(id=ss_profile.getId())

#         scores = []
#         for ss in request.data['skills']:
#             for skill in skills:
#                 if ss['name'] == skill.name:
#                     skill_data = {}
#                     skill_data['score'] = ss['score']
#                     scores.append(ss['score'])

#                     ss_serializer = SoftSkillSerializer(skill, data=skill_data, partial=True)
#                     ss_serializer.is_valid(raise_exception=True)
#                     ss_serializer.save()
#                 else:
#                     scores.append(skill.score)
        
#         # compute ss score
#         avg = 0.0
#         for score in scores:
#             sc = (score * 10) / 100
#             avg = avg + sc

#         serializer = SoftSkillProfileSerializer(
#             ss_profile, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    