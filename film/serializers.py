from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import *


class AktyorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ism = serializers.CharField()
    davlat = serializers.CharField()
    jins = serializers.CharField()
    tugulgan_yil = serializers.DateField()

    def validate_ism(self, qiymat):
        if len(qiymat) < 4:
            raise ValidationError("Ism-familiya bunday kalta bo'lmaydi")
        return qiymat

    def validate_jins(self, qiymat):
        if qiymat not in ["Erkak", "Ayol"]:
            raise ValidationError("Jins Erkak yoki Ayol bo'lishi shart")
        return qiymat


class TarifSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nom = serializers.CharField()
    narx = serializers.IntegerField()
    davomiylik = serializers.DurationField()


class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorSerializer(many=True)

    class Meta():
        model = Kino
        fields = '__all__'


class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorSerializer(many=True)

    class Meta():
        model = Kino
        fields = '__all__'

    def to_representation(self, instance):
        kino = super(KinoSerializer, self).to_representation(instance)
        kino.update({"aktyorlar_soni": len(kino.get("aktyorlar"))})
        kino.update({"izoh_soni": instance.izoh_set.all().count()})
        return kino


class KinoPostSerializer(serializers.ModelSerializer):
    class Meta():
        model = Kino
        fields = '__all__'


class IzohSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = '__all__'
