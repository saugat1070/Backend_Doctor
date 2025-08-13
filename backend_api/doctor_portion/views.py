from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.dateparse import parse_datetime
from doctor_portion.serializer import DoctorCreateSerializer, DoctorListSerializer
from doctor_portion.models import DoctorModel, BookingModel


class Create_Doctor(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response({
                'message': 'userId is not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Accept multipart/form-data (with optional file) or JSON
        serializer = DoctorCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'message': 'plaease enter valid information',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response({'message': 'DoctorInfo created Successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'DoctorInfo creation failed on Database!!'}, status=status.HTTP_403_FORBIDDEN)


class Fetch_Doctors(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = DoctorModel.objects.select_related('createdBy').all()
        if not doctors.exists():
            return Response({'message': 'There is no Doctor information'}, status=status.HTTP_404_NOT_FOUND)

        data = DoctorListSerializer(doctors, many=True, context={'request': request}).data
        return Response({'message': 'Doctor information fetching success', 'data': data}, status=status.HTTP_200_OK)


class Update_Doctor(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        # Validate that at least one field is truthy (mirrors Node.js logic)
        core_education = request.data.get('core_education')
        topic_education = request.data.get('topic_education')
        experience = request.data.get('experience')
        About = request.data.get('About')
        appointmentFee = request.data.get('appointmentFee')

        if not (core_education or topic_education or experience or About or appointmentFee):
            return Response({
                'message': 'At least one field must be provided for update'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = DoctorModel.objects.filter(id=id).first()
            if not doctor:
                return Response({'message': 'Doctor is not found!!!'}, status=status.HTTP_404_NOT_FOUND)

            # Apply provided fields (map camelCase to snake_case)
            if core_education is not None:
                doctor.core_education = core_education
            if topic_education is not None:
                doctor.topic_education = topic_education
            if experience is not None:
                try:
                    doctor.experience = int(experience)
                except (TypeError, ValueError):
                    return Response({'message': 'Invalid value for experience'}, status=status.HTTP_400_BAD_REQUEST)
            if About is not None:
                doctor.about = About
            if appointmentFee is not None:
                try:
                    doctor.appoint_fee = int(appointmentFee)
                except (TypeError, ValueError):
                    return Response({'message': 'Invalid value for appointmentFee'}, status=status.HTTP_400_BAD_REQUEST)

            doctor.save()
            return Response({'message': 'doctor information updated successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Error on database during update Doctor'}, status=status.HTTP_400_BAD_REQUEST)


class Delete_Doctor(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if not id:
            return Response({'message': 'doctor id should be provided!!'}, status=status.HTTP_400_BAD_REQUEST)

        doctor = DoctorModel.objects.filter(id=id).first()
        if not doctor:
            return Response({'message': 'Doctor is not found!!!'}, status=status.HTTP_404_NOT_FOUND)

        doctor.delete()
        return Response({'message': 'Doctor information deleted from dataBase!!!'}, status=status.HTTP_200_OK)


class Create_Booking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doctor_id):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response({'message': 'user id must be provided!'}, status=status.HTTP_400_BAD_REQUEST)

        # doctorId from path param
        if not doctor_id:
            return Response({'message': 'doctorId must be provided!'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse dateOfBooking (accept ISO 8601 string)
        date_str = request.data.get('dateOfBooking')
        if not date_str:
            return Response({'message': 'please provide booking information and paymentStatus'}, status=status.HTTP_400_BAD_REQUEST)

        booking_dt = parse_datetime(date_str)
        if booking_dt is None:
            return Response({'message': 'Invalid booking datetime'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure doctor exists
        doctor = DoctorModel.objects.filter(id=doctor_id).first()
        if not doctor:
            return Response({'message': 'Doctor is not found!!!'}, status=status.HTTP_404_NOT_FOUND)

        # Check for existing booking at the same time for this user
        existing = BookingModel.objects.filter(user=user, booking_date=booking_dt).exists()
        if existing:
            return Response({'message': 'At this time another booking is appeared!'}, status=status.HTTP_403_FORBIDDEN)

        try:
            booking = BookingModel.objects.create(
                doctor=doctor,
                user=user,
                booking_date=booking_dt,
            )
            return Response({'message': 'Booking successful', 'data': {
                'id': str(booking.id),
                'doctor': str(booking.doctor_id),
                'user': str(booking.user_id),
                'booking_date': booking.booking_date.isoformat()
            }}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_Bookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response({'message': 'user should be login'}, status=status.HTTP_400_BAD_REQUEST)

        qs = BookingModel.objects.select_related('doctor', 'user').filter(user=user)
        data = [
            {
                'id': str(b.id),
                'booking_date': b.booking_date.isoformat(),
                'user': {
                    'id': str(b.user.id),
                    'email': b.user.email,
                    'first_name': b.user.first_name,
                    'last_name': b.user.last_name,
                    'username': b.user.username,
                },
                'doctorInfo': {
                    'id': str(b.doctor.id),
                    'nameDoctor': b.doctor.name_doctor,
                    'core_education': b.doctor.core_education,
                    'topic_education': b.doctor.topic_education,
                    'experience': b.doctor.experience,
                    'About': b.doctor.about,
                    'appointmentFee': b.doctor.appoint_fee,
                }
            }
            for b in qs
        ]

        return Response({'message': 'Booking Cart is Successfully fetch!', 'data': data}, status=status.HTTP_200_OK)
