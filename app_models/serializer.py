from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import User



class ReviewSerializer(serializers.Serializer):

    class Meta:
        model = Review
        fields = ['all']
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user