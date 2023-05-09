from rest_framework.views import APIView
from rest_framework.response import Response

from student.serializers import WorkExpProfileSerializer, WorkExperienceSerializer
from student.models.workExpModels import WorkExpProfile, WorkExperience


class WorkExpProfileView(APIView):
    def get(self, *args, **kwargs):     # pass student_id
        # get work exp profile
        wx_profile = WorkExpProfile.objects.filter(id=self.kwargs['student_id']).first()
        serializer = WorkExpProfileSerializer(wx_profile)
        # get work experiences
        experiences = WorkExperience.objects.filter(id=wx_profile.wxProfileId)
        experiences_ser = WorkExperienceSerializer(experiences, many=True)
        # get work exp pie chart
        expIndustries = []
        expTimes = []
        for exp in experiences:
            if exp.wxpInd in expIndustries:
                idx = expIndustries.index(exp.industry)
                expTimes[idx] = expTimes[idx] + exp.timeSpent
            else:
                expIndustries.append(exp.industry)
                expTimes.append(exp.timeSpent)
        expPieChart = []
        for i, time in enumerate(expTimes):
            expTime = {}
            expTime['industry'] = expIndustries[i]
            expTime['time'] = time
            expPieChart.append(expTime)

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
    def post(self, request):      # pass workExp
        serializer = WorkExperienceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # update workExp Profile
        updateWxProfile(serializer.data['wx_profile'])

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):      # pass wxId & new workExp
        # update work experience object
        workExp = WorkExperience.objects.filter(id=self.kwargs['wxId']).first()
        serializer = WorkExperienceSerializer(workExp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # update workExp Profile
        updateWxProfile(workExp.wxProfileId)

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
    experiences = WorkExperience.objects.filter(id=wx_profile.wxProfileId)
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