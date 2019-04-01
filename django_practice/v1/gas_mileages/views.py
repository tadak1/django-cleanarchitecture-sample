import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt import authentication

from django_practice.gas_mileages.models import GasMileage
from django_practice.motorcycles.models import Motorcycle
from django_practice.users.models import User
from django_practice.v1.gas_mileages.serializers import V1GasMileageSearchSerializer, V1GasMileageResultSerializer, \
    V1GasMileageValidationSerializer
from django_practice.v1.users.serializers import V1UserResultSerializer, V1UserValidationSerializer, \
    V1MessageResultSerializer, V1ErrorMessageResultSerializer


class V1GasMileageView(APIView):
    authentication_classes = (authentication.JSONWebTokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(operation_summary='燃費リスト',
                         responses={200: V1GasMileageResultSerializer(), })
    def get(self, request):
        print(request.user)
        # ForeignKeyがつくものはManyをつけないとエラー
        serializers = V1GasMileageSearchSerializer()
        obj = serializers.search()
        result = V1GasMileageResultSerializer(obj)
        return Response(result.data, status=200)

    @swagger_auto_schema(operation_summary='燃費管理作成',
                         request_body=V1GasMileageValidationSerializer(),
                         responses={200: V1GasMileageResultSerializer(),
                                    400: V1ErrorMessageResultSerializer(), })
    def post(self, request):
        result = V1GasMileageValidationSerializer(data=request.data)
        if result.is_valid():
            user: User = User.objects.filter(username__contains='test').first()
            bike = result.validated_data['bike']
            motorcycle = Motorcycle.objects.filter(id=bike).first()
            gas_mileage: GasMileage = GasMileage(user_id=user.id)
            gas_mileage.trip = result.validated_data.get('trip', gas_mileage.trip)
            gas_mileage.price = result.validated_data['price']
            gas_mileage.amount = result.validated_data['amount']
            gas_mileage.refill_date = result.validated_data['refill_date']
            gas_mileage.remark = result.validated_data['remark']
            gas_mileage.save()
            # many to manyにaddする前にインスタンスをsaveしてレコードを生成する必要がある。
            gas_mileage.bike.add(motorcycle)
            gas_mileage.save()
            return Response({'message': 'ok'}, status=200)
        print(result.errors.__str__())
        return Response({'message': 'ng'})


class V1UserView(APIView):

    @swagger_auto_schema(operation_summary='ユーザー',
                         responses={200: V1UserResultSerializer(), })
    def get(self, request):
        # prefetchはgasmileageのUserIdをIn条件で検索している
        # users = User.object.prefetch_related(Prefetch('gasmileage_set',
        #                                               queryset=GasMileage.objects.all()))

        user = User.object.filter(username__contains='test').first()

        result = V1UserResultSerializer(user)
        return Response(result.data)

    @swagger_auto_schema(operation_summary='ユーザー',
                         request_body=V1UserValidationSerializer(),
                         responses={200: V1MessageResultSerializer(),
                                    400: V1ErrorMessageResultSerializer(), })
    def post(self, request):
        user = request.user
        bike = Motorcycle.objects.filter(name__contains='R1000').first()
        user.own.add(bike)
        user.save()
        return Response({'succeeded': True})
