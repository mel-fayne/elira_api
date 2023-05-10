import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

from rest_framework.views import APIView
from rest_framework.response import Response
from student.models.academicModels import AcademicProfile

from student.models.studentModels import Student
from student.models.technicalModels import TechnicalProfile
from student.models.workExpModels import WorkExpProfile
from student.serializers import StudentSerializer

JKUAT_CLASSIFIER_PATH = "/home/melfayne/elira_api/classifierModel/trainedModels/jkuatClassifier.pkl"
SPECIALISATIONS = ['AI','CS','DA','GD','HO','IS','NC','SD']

class ClassifierModelView(APIView):     # pass studentId
    def get(self, *args, **kwargs):
        # call required objects
        studentObj = Student.objects.filter(id=self.kwargs['student_id']).first()
        acdProfObj = AcademicProfile.objects.filter(student_id=self.kwargs['student_id']).first()
        groupingTotals = acdProfObj.csMarks
        techProfObj = TechnicalProfile.objects.filter(student_id=self.kwargs['student_id']).first()
        workProfObj = WorkExpProfile.objects.filter(student_id=self.kwargs['student_id']).first()

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
            'c': [techProfObj.cLang],
            'cmake': [techProfObj.cmakeLang],
            'c++': [techProfObj.cPlusPlusLang],
            'java': [techProfObj.javaLang],
            'javascript': [techProfObj.jsLang],
            'python': [techProfObj.pythonLang],
            'r': [techProfObj.rLang],
            'jupyter': [techProfObj.jupyterLang],
            'dart': [techProfObj.dartLang],
            'kotlin': [techProfObj.kotlinLang],
            'go': [techProfObj.goLang],
            'swift': [techProfObj.swiftLang],
            'c#': [techProfObj.cSharpLang],
            'aspNet': [techProfObj.aspNetLang],
            'typescript': [techProfObj.tsLang],
            'php': [techProfObj.phpLang],
            'objective_c': [techProfObj.objCLang],
            'ruby': [techProfObj.rubyLang],
            'html': [techProfObj.htmlLang],
            'css': [techProfObj.cssLang],
            'scss': [techProfObj.scssLang],
            'sql': [techProfObj.sqlLang],
            'rust': [techProfObj.rustLang],
            'internships_no': [workProfObj.internshipsNo],
            'time_spent': [workProfObj.timeSpent],
            'ai_industry': [workProfObj.aiInd],
            'cs_industry': [workProfObj.csInd],
            'da_industry': [workProfObj.daInd],
            'gd_industry': [workProfObj.gdInd],
            'ho_industry': [workProfObj.hoInd],
            'is_industry': [workProfObj.isInd],
            'na_industry': [workProfObj.naInd],
            'sd_industry': [workProfObj.sdInd]
        })

        student = student[['ai_industry', 'aspNet', 'c', 'c#', 'c++', 'cmake', 'cs01', 'cs02',
           'cs03', 'cs04', 'cs05', 'cs06', 'cs07', 'cs08', 'cs09', 'cs10', 'cs11',
           'cs12', 'cs13', 'cs14', 'cs15', 'cs16', 'cs17', 'cs18', 'cs_industry',
           'css', 'current_sem', 'da_industry', 'dart', 'gd_industry', 'go',
           'ho_industry', 'html', 'internships_no', 'is_industry', 'java',
           'javascript', 'jupyter', 'kotlin', 'na_industry', 'objective_c', 'php',
           'python', 'r', 'ruby', 'rust', 'scss', 'sd_industry', 'sql', 'swift',
           'time_spent', 'typescript']]

        # fit scaler
        data = pd.read_csv('/home/melfayne/elira_api/classifierModel/data/jkuatStudents.csv')
        main_cols = data.columns.difference(['studentId', 'school', 'specialisation'])
        X = data[main_cols]
        y = data['specialisation']
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        student = scaler.transform(student)     # transform student

        # Encode the target variable
        encoder = LabelEncoder()
        y_train = encoder.fit_transform(y_train)
        y_test = encoder.transform(y_test)

        # call model
        classifer_model = joblib.load(JKUAT_CLASSIFIER_PATH)
        preds = classifer_model.predict(student)
        preds = encoder.inverse_transform(preds)
        specialisation = preds[0]
        compatibilities = classifer_model.predict_proba(student)

        studentData = {}
        studentData['specialisation'] = specialisation
        compatibility_scores = {}
        for i, score in enumerate(compatibilities[0]):
            compatibility_scores[SPECIALISATIONS[i]] = score

        studentData['compatibility_scores'] = compatibility_scores
        studentData['specialisation_score'] = compatibility_scores[specialisation]

        print(studentData)

        #  update student predictions
        serializer = StudentSerializer(studentObj, data=studentData, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
