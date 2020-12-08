from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    # serializer without models for post request validation
    page = serializers.IntegerField()
    query = serializers.CharField()
