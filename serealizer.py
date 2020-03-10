from rest_framework import serializers


class ResultSerealizer(serializers.Serializer):
    city = serializers.CharField()
    price = serializers.IntegerField()
    square_all = serializers.IntegerField()
    square_live = serializers.IntegerField()
    square_kitchen = serializers.IntegerField()
    ad_type = serializers.CharField()
    floor = serializers.CharField()
    material = serializers.CharField()
    room = serializers.IntegerField()
    object_type = serializers.CharField()
    url = serializers.CharField()
    object_all_type = serializers.CharField()
