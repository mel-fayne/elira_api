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
        techProfObj = TechnicalProfile.objects.filter(id=self.kwargs['student_id']).first()
        workProfObj = WorkExpProfile.objects.filter(id=self.kwargs['student_id']).first()
        
        # prepare student dataframe
        student = pd.DataFrame({
            'current_sem': [acdProfObj.currentSem],
            'cs01': [acdProfObj.cs01],
            'cs02': [acdProfObj.cs02],
            'cs03': [acdProfObj.cs03],
            'cs04': [acdProfObj.cs04],
            'cs05': [acdProfObj.cs05],
            'cs06': [acdProfObj.cs06],
            'cs07': [acdProfObj.cs07],
            'cs08': [acdProfObj.cs08],
            'cs09': [acdProfObj.cs09],
            'cs10': [acdProfObj.cs1workProfObj],
            'cs11': [acdProfObj.cs11],
            'cs12': [acdProfObj.cs12],
            'cs13': [acdProfObj.cs13],
            'cs14': [acdProfObj.cs14],
            'cs15': [acdProfObj.cs15],
            'cs16': [acdProfObj.cs16],
            'cs17': [acdProfObj.cs17],
            'cs18': [acdProfObj.cs18],
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
    