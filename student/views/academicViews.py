from rest_framework.views import APIView
from rest_framework.response import Response

from student.models.academicModels import AcademicProfile, SchoolGrouping, SchoolUnit, StudentUnit
from student.serializers import AcademicProfileSerializer, GetStudentUnitSerializer, SchoolGroupingSerializer, SchoolUnitSerializer, StudentUnitSerializer

GROUPINGS = ['cs01', 'cs02', 'cs03', 'cs04', 'cs05', 'cs06', 'cs07', 'cs08',
             'cs09', 'cs10', 'cs11', 'cs12', 'cs13', 'cs14', 'cs15', 'cs16', 'cs17', 'cs18']

SEMESTERS = [1.0, 1.1, 1.2, 2.0, 2.1, 2.2, 3.0, 3.1, 3.2, 4.0, 4.1, 4.2]


class AcademicProfileView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        ac_profile = AcademicProfile.objects.filter(
            student_id=self.kwargs['student_id']).first()
        serializer = AcademicProfileSerializer(ac_profile)
        acData = {}
        acData['ac_profile'] = serializer.data
        acData['student_units'] = getSortedUnitGroups(ac_profile.acProfileId)
        return Response(acData)

    def post(self, request):    # pass current_sem, school & student_id
        # create academic profile
        serializer = AcademicProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # create student units
        # get school units needed to create student units
        schoolUnitObjs = SchoolUnit.objects.filter(school=request.data['school'])
        ac_profileId = AcademicProfile.objects.filter(
            student_id=request.data['student_id']).first().acProfileId
        for unit in schoolUnitObjs:
            studentUnit = {}
            studentUnit['ac_profile'] = ac_profileId
            studentUnit['school_unit'] = unit.schoolUnitId
            serializer = StudentUnitSerializer(data=studentUnit)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # return empty transcripts for previous semseters
        empty_transcripts = {}
        prev_semesters = getSemesters(request.data['current_sem'])
        studentUnitObjs = StudentUnit.objects.filter(ac_profile=ac_profileId)
        for sem in prev_semesters:
            units = []
            for unit in studentUnitObjs:
                if unit.unitSem == sem:
                    serializer = GetStudentUnitSerializer(unit)
                    units.append(serializer.data)
            empty_transcripts[sem] = units

        return Response(empty_transcripts)

class StudentTranscript(APIView):     # pass student_id, new_sem
    def get(self, *args, **kwargs):
        empty_transcript = {}
        ac_profileId = AcademicProfile.objects.filter(student_id=self.kwargs['student_id']).first().acProfileId
        new_sem = float(self.kwargs['new_sem'])
        studentUnitObjs = StudentUnit.objects.filter(ac_profile=ac_profileId)

        units = []
        for unit in studentUnitObjs:
            if unit.unitSem == new_sem:
                serializer = GetStudentUnitSerializer(unit)
                units.append(serializer.data)

        empty_transcript[new_sem] = units

        return Response(empty_transcript)


class StudentUnitView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        ac_profile = AcademicProfile.objects.filter(
            student_id=self.kwargs['student_id']).first()
        ac_profileId = ac_profile.acProfileId
        current_sem = ac_profile.currentSem
        unitsData = {}
        allSemData = {}
        semAvgs = []
        index = 0

        for sem in SEMESTERS:
            semData = {}
            if sem < current_sem:
                units = StudentUnit.objects.filter(ac_profile=ac_profileId)
                semUnits = []
                for unit in units:
                    if unit.unitSem == sem:
                        serializer = GetStudentUnitSerializer(unit)
                        semUnits.append(serializer.data)

                semData['allUnits'] = semUnits

                if len(semUnits) != 0:
                    total = 0.0
                    for unit in semUnits:
                        total = total + unit['mark']
                    if total == 0.0:
                        semData['average'] = 0.0
                        semAvgs.append(semData['average'])
                    else:
                        semData['average'] = round((total / len(semUnits)), 2)
                        semAvgs.append(semData['average'])
                    semData['honours'] = getHonours(semData['average'])
                    if len(semAvgs) == 0:
                        pass
                    else:
                        diff = semAvgs[index] - semAvgs[index - 1]
                        if diff == 0 or semAvgs[index - 1] == 0:
                            semData['status'] = 'Same'
                            semData['difference'] = 0
                        else:
                            if diff < 0:
                                semData['status'] = 'Drop'
                                diff = semAvgs[index - 1] -  semAvgs[index]
                            else:
                                semData['status'] = 'Up'

                            semData['difference'] = round(((diff / semAvgs[index - 1]) * 100), 1)

                    allSemData[sem] = semData
                    index = index + 1
                else:
                    pass

            else:
                pass

        unitsData['semData'] = allSemData
        unitsData['semAvgs'] = semAvgs

        profileData = {}
        avgTotal = 0.0
        for avg in semAvgs:
            avgTotal = avgTotal + avg
        if len(semAvgs) == 0:
            profileData['current_avg'] = avgTotal
        else:
            profileData['current_avg'] = avgTotal / len(semAvgs)
        profileData['current_honours'] = getHonours(profileData['current_avg'])

        acp_serializer = AcademicProfileSerializer(ac_profile, data=profileData, partial=True)
        acp_serializer.is_valid(raise_exception=True)
        acp_serializer.save()

        return Response(unitsData)


    def patch(self, request, *args, **kwargs):      # pass studentId and student unit objects
        ac_profile = AcademicProfile.objects.filter(student_id=self.kwargs['student_id']).first()
        ac_profileId = ac_profile.acProfileId
        current_sem = request.data['current_sem']
        studentUnits = request.data['studentUnits']

        # update StudentUnit objects
        for unit in studentUnits:
            unitObj = StudentUnit.objects.filter(id=unit['id']).first()
            serializer = StudentUnitSerializer(
                unitObj, data=unit, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        ac_profile = AcademicProfile.objects.filter(id=ac_profileId).first()
        acp_serializer = AcademicProfileSerializer(ac_profile, data={'current_sem': current_sem}, partial=True)
        acp_serializer.is_valid(raise_exception=True)
        acp_serializer.save()

        # return sorted list of student units grouped by unitGrouping
        unitsData = getSortedUnitGroups(ac_profileId)

        return Response(unitsData)


class SchoolUnitView(APIView):
    def get(self, *args, **kwargs):
        groupBy = self.kwargs['groupBy']
        school = self.kwargs['school']
        schoolUnits = {}

        if groupBy == 'semester':
            for sem in SEMESTERS:
                units = SchoolUnit.objects.filter(school=school, semester=sem)
                serializer = SchoolUnitSerializer(units, many=True)
                schoolUnits[sem] = serializer.data

        else:
            unitObjects = SchoolUnit.objects.filter(school=school)

            for grouping in GROUPINGS:
                groupUnits = []
                for unit in unitObjects:
                    groupCodes = unit.groupCodes
                    for i, code in enumerate(groupCodes):
                        if code == grouping:
                            serializer = SchoolUnitSerializer(unit)
                            groupUnits.append(serializer.data)
                        else:
                            pass

                schoolUnits[grouping] = groupUnits

        return Response(schoolUnits)

    def post(self, request):
        serializer = SchoolUnitSerializer(data=request.data['schoolUnits'], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('All Units Uploaded Successfully')


class UnitGroupsView(APIView):
    def post(self, request):
        serializer = SchoolGroupingSerializer(data=request.data['unitGroups'], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ------------------------------- Util Functions -----------------------------


def getSemesters(current_sem):
    prev_sems = []
    for sem in SEMESTERS:
        if current_sem == sem:
            break
        else:
            prev_sems.append(sem)

    return prev_sems


def getHonours(average):
    honours = ''

    if average >= 70:
        honours = 'First Class'
    elif average < 70 and average >= 60:
        honours = 'Second Upper'
    elif average < 60 and average >= 50:
        honours = 'Second Lower'
    elif average < 50 and average > 40:
        honours = 'Pass'
    else:
        honours = 'Fail'

    return honours

def getSortedUnitGroups(ac_profileId):
    ac_profile = AcademicProfile.objects.filter(id=ac_profileId).first()
    unitsData = {}
    groupingTotals = []
    groupingNames = GROUPINGS[:]
    groupingObjs = SchoolGrouping.objects.filter(school=ac_profile.studentSchool)
    studentUnitObjs = StudentUnit.objects.filter(ac_profile=ac_profileId)

    for i, grouping in enumerate(groupingNames):
        groupingData = {}
        groupingData['code'] = grouping
        groupingObj = groupingObjs[0]
        for obj in groupingObjs:
            if obj.groupCode == grouping:
                groupingObj = obj
        groupingData['unit_perc'] = groupingObj.unitPerc

        # compute group units
        groupUnits = []
        groupUnitsMarks = []
        for unit in studentUnitObjs:
            groupCodes = unit.groupCodes
            for i, code in enumerate(groupCodes):
                if code == grouping:
                    serializer = GetStudentUnitSerializer(unit)
                    groupUnits.append(serializer.data)
                    groupUnitsMarks.append(unit.unitMark)
                else:
                    pass

        if len(groupUnits) == 0:
            groupingData['units'] = []
            groupingData['completeness'] = 0.0
        else:
            zippedLists = zip(groupUnits, groupUnitsMarks)
            sortedZippedLists = sorted(zippedLists, key=lambda x: x[0]['mark'], reverse=True)
            sortedUnits, sortedMarks = zip(*sortedZippedLists)

            groupingData['units'] = sortedUnits
            count = 0
            for unit in sortedUnits:
                if unit['mark'] > 0:
                    count = count + 1

            groupingData['completeness'] = round((count * groupingObj.unit_percentage))

        # compute group totals
        total = 0.0
        for mark in groupUnitsMarks:
            total = total + ((mark * groupingObj.unitPerc ) / 100)
        total = round(total, 2)
        groupingTotals.append(total)
        groupingData['total'] = total

        if total == 0.0:
            pass
        else:
            unitsData[grouping] = groupingData

    # update academic profile
    profileData = {}
    for i, grouping in enumerate(GROUPINGS):
        profileData[grouping] = groupingTotals[i]
    ac_profile = AcademicProfile.objects.filter(id=ac_profileId).first()
    acp_serializer = AcademicProfileSerializer(ac_profile, data=profileData, partial=True)
    acp_serializer.is_valid(raise_exception=True)
    acp_serializer.save()

    return unitsData
