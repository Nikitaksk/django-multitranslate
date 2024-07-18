from rest_framework import serializers

class textSerializer(serializers.Serializer):
    data = serializers.CharField()
