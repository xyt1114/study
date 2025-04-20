# serializers.py
from rest_framework import serializers

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'video_file', 'uploaded_at']
