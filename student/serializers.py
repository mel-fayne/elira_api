from rest_framework import serializers


from student.models.authModels import Student
from student.models.academicModels import AcademicProfile, SchoolUnit, StudentUnit

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name', 'last_name',
            'email',
            'password',
            'news_history'
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


class StudentUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUnit
        fields = '__all__'