import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

from rest_framework.views import APIView
from rest_framework.response import Response
from student.models.academicModels import AcademicProfile

from student.models.studentModels import Student
from student.models.technicalModels import TechnicalProfile
from student.models.workExpModels import WorkExpProfile
from student.serializers import StudentSerializer

JKUAT_CLASSIFIER_PATH = "/home/mel/Desktop/code-lab/api/elira_api/classifierModel/trainedModels/jkuatClassifier.pkl"
SPECIALISATIONS = ['AI','CS','DA','GD','HO','IS','NC','SD']

class ClassifierModelView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        # call required objects
        studentObj = Student.objects.filter(id=self.kwargs['student_id']).first()
        acdProfObj = AcademicProfile.objects.filter(id=self.kwargs['student_id']).first()
        groupingTotals = acdProfObj.csMarks
        techProfObj = TechnicalProfile.objects.filter(id=self.kwargs['student_id']).first()
        workProfObj = WorkExpProfile.objects.filter(id=self.kwargs['student_id']).first()
        
        # prepare student dataframe
        student = pd.DataFrame({
            'current_sem': [acdProfObj.currentSem],
            'cs01': [groupingTotals[0]],
            'cs02': [groupingTotals[1]],
            'cs03': [groupingTotals[2]],
            'cs04': [groupingTotals[3]],
            'cs05': [groupingTotals[4]],
            'cs06': [groupingTotals[5]],
            'cs07': [groupingTotals[6]],
            'cs08': [groupingTotals[7]],
            'cs09': [groupingTotals[8]],
            'cs10': [groupingTotals[9]],
            'cs11': [groupingTotals[10]],
            'cs12': [groupingTotals[11]],
            'cs13': [groupingTotals[12]],
            'cs14': [groupingTotals[13]],
            'cs15': [groupingTotals[14]],
            'cs16': [groupingTotals[15]],
            'cs17': [groupingTotals[16]],
            'cs18': [groupingTotals[17]],
            'c': [techProfObj.c],
            'c++': [techProfObj.cPlusPlus],
            'java': [techProfObj.java],
            'javascript': [techProfObj.javascript],
            'python': [techProfObj.python],
            'r': [techProfObj.r],
            'jupyter': [techProfObj.jupyter],
            'dart': [techProfObj.dart],
            'kotlin': [techProfObj.kotlin],
            'go': [techProfObj.go],
            'swift': [techProfObj.swift],
            'c#': [techProfObj.cSharp],
            'typescript': [techProfObj.typescript],
            'php': [techProfObj.php],
            'objective_c': [techProfObj.objective_c],
            'ruby': [techProfObj.ruby],
            'html': [techProfObj.html],
            'css': [techProfObj.css],
            'sql': [techProfObj.sql],
            'rust': [techProfObj.rust],
            'internships_no': [workProfObj.internshipsNo],
            'time_spent': [workProfObj.timeSpent],
            'ai_industry': [workProfObj.ai_industry],
            'cs_industry': [workProfObj.cs_industry],
            'da_industry': [workProfObj.da_industry],
            'gd_industry': [workProfObj.gd_industry],
            'ho_industry': [workProfObj.ho_industry],
            'is_industry': [workProfObj.is_industry],
            'na_industry': [workProfObj.na_industry],
            'sd_industry': [workProfObj.sd_industry]
        })
        
        student = student[['ai_industry', 'c', 'c#', 'c++', 'cs01', 'cs02', 'cs03', 'cs04', 'cs05',
       'cs06', 'cs07', 'cs08', 'cs09', 'cs10', 'cs11', 'cs12', 'cs13', 'cs14',
       'cs15', 'cs16', 'cs17', 'cs18', 'cs_industry', 'css', 'current_sem',
       'da_industry', 'dart', 'gd_industry', 'go', 'ho_industry', 'html',
       'internships_no', 'is_industry', 'java', 'javascript', 'jupyter',
       'kotlin', 'na_industry', 'objective_c', 'php', 'python', 'r', 'ruby',
       'rust', 'sd_industry', 'sql', 'swift', 'time_spent', 'typescript']]
        scaler = StandardScaler()
        student = scaler.transform(student)
        
        # call model
        classifer_model = joblib.load(JKUAT_CLASSIFIER_PATH)
        specialisation = classifer_model.predict(student)[0]
        compatibilities = classifer_model.predict_proba(student)
        
        studentData = {}
        studentData['specialisation'] = specialisation
        studentData['compatibility_scores'] = compatibilities
        studentData['specialisation_score'] = compatibilities[SPECIALISATIONS.index(specialisation)]

        #  update student predictions
        serializer = StudentSerializer(studentObj, data=studentData, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    