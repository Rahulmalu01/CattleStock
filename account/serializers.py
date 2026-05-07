from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'organization', 'timezone', 'language',
            'email_verified', 'phone_verified', 'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['email_verified', 'phone_verified', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirm Password')
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    organization = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2',
                  'phone_number', 'organization']

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        phone = validated_data.pop('phone_number', '')
        org = validated_data.pop('organization', '')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'phone_number': phone, 'organization': org}
        )
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number', 'organization', 'timezone', 'language',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        # Update User fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': 'Passwords do not match.'})
        return data
