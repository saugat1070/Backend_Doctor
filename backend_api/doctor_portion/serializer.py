from rest_framework import serializers
from doctor_portion.models import DoctorModel
from Authentication.models import User


class DoctorCreateSerializer(serializers.ModelSerializer):
    # Map request body keys to model fields
    nameDoctor = serializers.CharField(source='name_doctor')
    About = serializers.CharField(source='about')
    appointmentFee = serializers.IntegerField(source='appoint_fee')
    profileDoc = serializers.ImageField(source='profile_doctor', required=False, allow_null=True)

    class Meta:
        model = DoctorModel
        fields = [
            'nameDoctor',
            'core_education',
            'topic_education',
            'experience',
            'About',
            'appointmentFee',
            'profileDoc',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            # Match the original message semantics
            raise serializers.ValidationError({'message': 'userId is not found'})

        # Default profile image if not provided (mirrors the Node.js behavior)
        if not validated_data.get('profile_doctor'):
            # Store the URL string as the file name reference, consistent with the provided code
            validated_data['profile_doctor'] = 'http://localhost:3000/doctorProfile.png'

        # Attach creator
        return DoctorModel.objects.create(createdBy=user, **validated_data)


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'username', 'photo_name', 'date_of_birth', 'role'
        )


class DoctorListSerializer(serializers.ModelSerializer):
    nameDoctor = serializers.CharField(source='name_doctor')
    About = serializers.CharField(source='about', allow_blank=True, allow_null=True)
    appointmentFee = serializers.IntegerField(source='appoint_fee')
    profileDoc = serializers.SerializerMethodField()
    # Expose related user as `user`, excluding password & admin flags
    user = UserPublicSerializer(source='createdBy', read_only=True)

    class Meta:
        model = DoctorModel
        fields = (
            'id', 'nameDoctor', 'core_education', 'topic_education', 'experience', 'About', 'appointmentFee', 'profileDoc', 'is_available', 'user'
        )

    def get_profileDoc(self, obj):
        # If it's an ImageField with a file, build absolute URL; if it's a stored URL string, return as-is
        try:
            request = self.context.get('request')
            if hasattr(obj.profile_doctor, 'url'):
                url = obj.profile_doctor.url
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
            # Fallback if a raw string was stored
            return obj.profile_doctor
        except Exception:
            return None


