from rest_framework import serializers
from Authentication.models import User
from django.contrib.auth.hashers import make_password

class SignUp(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        data.pop("confirm_password")  
        return data
    
    

class Profile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'email', 'first_name', 'last_name', 'photo_name', 'username', 'date_of_birth']
        read_only = ["id","email","username"]

class CreateUserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'fullName']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'email': {'required': True},
        }

    def validate(self, attrs):
        full_name = attrs.get('fullName')
        if not full_name or ' ' not in full_name.strip():
            # Accept single token as first_name and blank last_name
            pass
        return attrs

    def create(self, validated_data):
        full_name = validated_data.pop('fullName', '')
        parts = [p for p in full_name.strip().split(' ') if p]
        first = parts[0] if parts else ''
        last = ' '.join(parts[1:]) if len(parts) > 1 else ''
        password = validated_data.pop('password')
        return User.objects.create_user(first_name=first, last_name=last, password=password, **validated_data)


