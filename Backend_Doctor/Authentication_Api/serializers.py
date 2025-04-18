from rest_framework import serializers
from Authentication_Api.models import UserRegistration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = '__all__'
    
    def create(self,validated_data):
        user = UserRegistration(
            email = validated_data['email'],
            name = validated_data['name']            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user