from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerialier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DetailsSerialier(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class UnitSerialier(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LoginSerialier(serializers.ModelSerializer):  #----Excluded User Serializer
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','is_active']


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = '__all__'

class ProductSerialier(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SelectedProductserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','featured','discount']

class ProductDetailsSerialier(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth =1

class UserDetailsSerializer(serializers.ModelSerializer):
    username = LoginSerialier()
    class Meta:
        model = UserDetails
        depth =1
        exclude =('id',)

class ShipperSerializer(serializers.ModelSerializer):
    delivary_boy = LoginSerialier()
    class Meta:
        model = Shipper
        fields = '__all__'
        depth =1

class AllOrderSerializer(serializers.ModelSerializer):  #---------Odrer Details Getting Serializer
    username = LoginSerialier()
    shipper = ShipperSerializer()
    class Meta:
        model = Order
        fields = '__all__'
        depth =1

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class GetAddressSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    class Meta:
        model = Address
        fields = '__all__'

class AddOrderDetailsSeializer(serializers.ModelSerializer): #-------insertsection
    class Meta:
        model = OrderDeatails
        fields = '__all__'

class OrderDetailsSeializer(serializers.ModelSerializer):
    order = AllOrderSerializer()
    class Meta:
        model = OrderDeatails
        fields = '__all__'
        depth = 2

class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipper
        fields = '__all__'

class DelivaryDashBoarSerilaizer(serializers.Serializer):
    total = serializers.IntegerField()
    completed = serializers.IntegerField()
    amount = serializers.FloatField()
    shipper__delivary_boy__first_name = first_name = serializers.CharField(max_length=20)
    shipper__delivary_boy__last_name = last_name = serializers.CharField(max_length=20)

class ProducaReportSerializer(serializers.Serializer):
    qty_sum = serializers.IntegerField()
    amount = serializers.FloatField()
    product__name = product = serializers.CharField(max_length=20)
    product__unit__unit = unit = serializers.CharField(max_length=20)
    product__id = id = serializers.IntegerField()

class OrderReportSerializer(serializers.ModelSerializer):
    username =LoginSerialier()
    class Meta:
        model = Order
        fields = ['inv_number','username','total_amount','payment_type','shiping_charge']
        depth =1

class DelivaryReportSerilaizer(serializers.Serializer):
    total = serializers.IntegerField()
    completed = serializers.IntegerField()
    cod_amount = serializers.FloatField()
    upi_amount = serializers.FloatField()
    shiping_charge = serializers.FloatField()
    shipper__delivary_boy__first_name = first_name = serializers.CharField(max_length=20)
    shipper__delivary_boy__last_name = last_name = serializers.CharField(max_length=20)

class IncomeReportSerilaizer(serializers.Serializer):
    total = serializers.IntegerField()
    completed = serializers.IntegerField()
    pending = serializers.IntegerField()
    canceled = serializers.IntegerField()
    shiping_charge = serializers.FloatField()
    cod_amount = serializers.FloatField()
    upi_amount = serializers.FloatField()

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class DelivaryBoysOrderSerializer(serializers.ModelSerializer):
    # username = LoginSerialier()
    address = AddressSerializer()
    class Meta:
        model = Order
        exclude =('shipper','delivary_date','delivary_remarks','location','username')
        depth =1

#------------------User Section -----------------------------#

class UserProductSerializer(serializers.ModelSerializer):
    catagory = serializers.StringRelatedField()
    unit = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'

class AllIncomeReportSerilaizer(serializers.Serializer):
    location__name =location = serializers.CharField()
    total = serializers.IntegerField()
    completed = serializers.IntegerField()
    pending = serializers.IntegerField()
    canceled = serializers.IntegerField()
    shiping_charge = serializers.FloatField()
    cod_amount = serializers.FloatField()
    upi_amount = serializers.FloatField()
