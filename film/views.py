from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_201_CREATED
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
        soz = request.query_params.get("ism")
        davlati = request.query_params.get("davlat")
        tartib = request.query_params.get("order")
        pagination_class = PageNumberPagination
        pagination_class.page_size = 3
        paginator = PageNumberPagination()
        if soz:
            aktyorlar = aktyorlar.filter(ism__contains=soz)
        if davlati:
            aktyorlar = aktyorlar.filter(davlat=davlati)
        if tartib:
            aktyorlar = aktyorlar.order_by(tartib)
        paginated_queryset = paginator.paginate_queryset(aktyorlar, request)
        serializer = AktyorSerializer(paginated_queryset, many=True)
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
            return Response(natija)
            # Bu yerda <serializer.data> buni qoysam eski natijani qaytarb qo'yyapti  shu sababli btta natija qaytaryapman
        return Response(serializer.errors)


class KinolarAPi(APIView):
    def get(self, request):
        kinolar = Kino.objects.all()
        serializer = KinoSerializer(kinolar, many=True)
        return Response(serializer.data)

    def post(self, request):
        kino = request.data
        serializer = KinoPostSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class KinoAPi(APIView):
    def get(self, request, pk):
        kino = Kino.objects.get(id=pk)
        serializer = KinoSerializer(kino)
        return Response(serializer.data)


class IzohModelViewSet(ModelViewSet):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["sana"]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     return serializer

    # def retrieve(self, request, *args, **kwargs):
    #     izoh = self.get_object()
    #     if izoh < 5:
    #         return Response
    #     return Response

    # def destroy(self, request, *args, **kwargs):
    #     pass


class KinoModelViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoPostSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1

    # def list(self, request, *args, **kwargs):  # hammasini get qilish uchun
    #     kinolar = self.queryset
    #     serializer = KinoSerializer(kinolar, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):  # bttasini get qilish uchun
        kino = self.get_object()
        serializer = KinoSerializer(kino)
        return Response(serializer.data)

    @action(detail=True)  # movies/pk/izohlar
    def izohlar(self, request, pk):
        kino = self.get_object()
        kino_izohlar = kino.izoh_set.all()
        serializer = IzohSerializer(kino_izohlar, many=True)
        return Response(serializer.data)

    @action(detail=True)  # movies/pk/aktyorlar
    def aktyorlar(self, request, pk):
        kino = self.get_object()
        kino_aktyor = kino.aktyorlar.all()
        serializer = AktyorSerializer(kino_aktyor, many=True)
        return Response(serializer.data)


class AktyorModelViewSet(ModelViewSet):
    queryset = Aktyor.objects.all()
    serializer_class = AktyorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'ism', 'davlat']  # /?search=.....
    ordering_fields = ['id', 'ism', "tugulgan_yil"]  # /?ordering=....

    def get_queryset(self):
        aktyorlar = self.queryset
        gender = self.request.query_params.get('jins')
        if gender:
            aktyorlar = aktyorlar.filter(jins=gender)
        return aktyorlar


class IzohListCreateAPIView(ListCreateAPIView):
    serializer_class = IzohSerializer2
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Izoh.objects.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return HTTP_201_CREATED
