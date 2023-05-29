from rest_framework.views import APIView
from rest_framework.response import Response

from student.serializers import WorkExpProfileSerializer, WorkExperienceSerializer
from student.models.workExpModels import WorkExpProfile, WorkExperience


class WorkExpProfileView(APIView):
    def get(self, *args, **kwargs):     # pass student_id
        # update workExp Profile
        wxProfileId = WorkExpProfile.objects.filter(student_id=self.kwargs['student_id']).first().wxProfileId
        updateWxProfile(wxProfileId)

        # get work experiences
        experiences = WorkExperience.objects.filter(wx_profile=wxProfileId)
        experiences_ser = WorkExperienceSerializer(experiences, many=True)

        # get work exp profile
        wx_profile= WorkExpProfile.objects.filter(id=wxProfileId).first()
        serializer = WorkExpProfileSerializer(wx_profile)
        totalTime = wx_profile.timeSpent

         # get work exp pie chart
        expIndustries = []
        expTimes = []
        expPieChart = {}
        for exp in experiences:
            expIndustries.append(exp.industry)
            expTimes.append(exp.timeSpent)

        for i, ind in enumerate(expIndustries):
            if ind in expPieChart:
                expPieChart[ind] = expPieChart[ind] + expTimes[i]
            else:
                expPieChart[ind] = expTimes[i]

        for ind in expPieChart:
            expPieChart[ind] = round(((expPieChart[ind] / totalTime) * 100), 2)

        wxData = {}
        wxData['wx_profile'] = serializer.data
        wxData['experiences'] = experiences_ser.data
        wxData['expPieChart'] = expPieChart

        return Response(wxData)

    def post(self, request):    # pass studentId
        serializer = WorkExpProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class WorkExperienceView(APIView):
    def post(self, request):      # pass student_id & workExp
        wx_profileId = WorkExpProfile.objects.filter(student_id=request.data['student_id']).first().wxProfileId
        workExpData = request.data['workExp']
        workExpData['wx_profile'] = wx_profileId
        serializer = WorkExperienceSerializer(data=workExpData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):      # pass wxId & new workExp
        # update work experience object
        workExp = WorkExperience.objects.filter(id=self.kwargs['wxId']).first()
        serializer = WorkExperienceSerializer(workExp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, *args, **kwargs):      # pass wxId
        # update workExp Profile
        workExp = WorkExperience.objects.filter(id=self.kwargs['wxId']).first()
        wx_profile = WorkExpProfile.objects.filter(id=workExp.wxProfileId).first()

        wxData = {}
        wxData['internships_no'] = wx_profile.internshipsNo - 1
        wxData['time_spent'] = wx_profile.timeSpent - workExp.timeSpent

        serializer = WorkExpProfileSerializer(wx_profile, data=wxData, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # delete Work Exp Object
        WorkExperience.objects.filter(id=self.kwargs['wxId']).delete()

        return Response('Deleted Successfully')


def updateWxProfile(wxProfileId):
    wx_profile = WorkExpProfile.objects.filter(id=wxProfileId).first()

    wxData = {}
    experiences = WorkExperience.objects.filter(wx_profile=wx_profile.wxProfileId)
    wxData['internships_no'] = len(experiences)
    timeSpent = 0
    for exp in experiences:
        timeSpent += exp.timeSpent
        if exp.wxpInd == 'sd_industry':
            wxData['sd_industry'] = 1
        if exp.wxpInd == 'na_industry':
            wxData['na_industry'] = 1
        if exp.wxpInd == 'ai_industry':
            wxData['ai_industry'] = 1
        if exp.wxpInd == 'cs_industry':
            wxData['cs_industry'] = 1
        if exp.wxpInd == 'da_industry':
            wxData['da_industry'] = 1
        if exp.wxpInd == 'ho_industry':
            wxData['ho_industry'] = 1
        if exp.wxpInd == 'is_industry':
            wxData['is_industry'] = 1
        if exp.wxpInd == 'gd_industry':
            wxData['gd_industry'] = 1

    wxData['time_spent'] = timeSpent

    serializer = WorkExpProfileSerializer(wx_profile, data=wxData, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()