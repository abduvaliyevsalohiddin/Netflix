from rest_framework import serializers


class AktyorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ism = serializers.CharField()
    davlat = serializers.CharField()
    jins = serializers.CharField()
    tugulgan_yil = serializers.DateField()


class TarifSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nom = serializers.CharField()
    narx = serializers.IntegerField()
    davomiylik = serializers.DurationField()
