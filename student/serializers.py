from rest_framework import serializers


from student.models.studentModels import Student
from student.models.academicModels import AcademicProfile, SchoolGrouping, SchoolUnit, StudentUnit
from student.models.softSkillsModels import SoftSkillProfile, SoftSkill
from student.models.technicalModels import TechnicalProfile
from student.models.workExpModels import WorkExpProfile, WorkExperience

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name', 'last_name',
            'specialisation',
            'specialisation_score',
            'compatibility_scores',
            'email',
            'password',
            'project_wishlist',
            'last_active', 'user_token',
            'first_pet',
            'childhood_street',
            'first_teacher',
            'favourite_flavour',
            'childhod_nickname',
            'first_phone'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class AcademicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicProfile
        fields = '__all__'


class SchoolUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolUnit
        fields = '__all__'

class SchoolGroupingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGrouping
        fields = '__all__'


class StudentUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUnit
        fields = '__all__'

class GetStudentUnitSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source='school_unit.name')
    unit_codes = serializers.CharField(source='school_unit.grouping_code')
    unit_perc = serializers.CharField(source='school_unit.unit_percentages')
    class Meta:
        model = StudentUnit
        fields = [
            'id',
            'ac_profile',
            'school_unit',
            'grade',
            'mark',
            'unit_name',
            'unit_codes',
            'unit_perc'
        ]

class TechnicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalProfile
        fields = '__all__'


class WorkExpProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExpProfile
        fields = '__all__'


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


class SoftSkillProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkillProfile
        fields = '__all__'


class SoftSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkill
        fields = '__all__'
