from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class HelleApi(APIView):
    def get(self, request):
        d = {
            "xabar": "Salom, Dunyo!",
            "izoh": "Test uchun Api yozdik"
        }
        return Response(d)

    def post(self, request):
        d = request.data
        natija = {
            "xabar": "Post qabul qilindi",
            "post ma'lumoti": d
        }
        return Response(natija)


class AktyorlarAPi(APIView):
    def get(self, request):
        aktyorlar = Aktyor.objects.all()
        serializer = AktyorSerializer(aktyorlar, many=True)
        return Response(serializer.data)

    def post(self, request):
        aktyor = request.data
        serializer = AktyorSerializer(data=aktyor)
        if serializer.is_valid():
            data = serializer.validated_data
            Aktyor.objects.create(
                ism=data.get("ism"),
                davlat=data.get("davlat"),
                jins=data.get("jins"),
                tugulgan_yil=data.get("tugulgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class AktyorAPi(APIView):
    def get(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor)
        return Response(serializer.data)

    def update(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Aktyor.objects.filter(id=pk).update(
                ism=data.get("ism"),
                davlat=data.get("davlat"),
                jins=data.get("jins"),
                tugulgan_yil=data.get("tugulgan_yil"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class TariflarAPi(APIView):
    def get(self, request):
        tariflar = Tarif.objects.all()
        serializer = TarifSerializer(tariflar, many=True)
        return Response(serializer.data)

    def post(self, request):
        tarif = request.data
        serializer = TarifSerializer(data=tarif)
        if serializer.is_valid():
            data = serializer.validated_data
            Tarif.objects.create(
                nom=data.get("nom"),
                narx=data.get("narx"),
                davomiylik=data.get("davomiylik"),
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class TarifAPi(APIView):
    def get(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(tarif)
        return Response(serializer.data)

    def delete(self, request, pk):
        Tarif.objects.filter(id=pk).delete()
        natija = {
            "xabar": "Tanlangan tarif o'chirildi",
        }
        return Response(natija)

    def put(self, request, pk):
        tarif = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(tarif, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Tarif.objects.filter(id=pk).update(
                nom=data.get('nom'),
                narx=data.get('narx'),
                davomiylik=data.get('davomiylik')
            )
            natija = {
                "xabar": "Tanlangan tarif update bo'ldi",
            }
            return Response(
                natija)  # Bu yerda <serializer.data> buni qoysam eski natijani qaytarb qo'yyapti  shu sababli btta natija qaytaryapman
        return Response(serializer.errors)
