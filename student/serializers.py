from rest_framework import serializers

from student.models import Student, TechnicalProfile


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
            'isVerified', 'verify_otp',
            'reset_otp', 'reset_expiry']
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


class TechnicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalProfile
        fields = '__all__'