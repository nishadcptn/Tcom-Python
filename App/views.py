from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path,os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.permissions import IsAuthenticated    #------- For Authentication --------#
from .models import *
from django.conf import settings
from PIL import Image as images
from .serializer import *
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.permissions import IsAuthenticated
import random
from datetime import datetime
from django.db.models import Count, F, Value, OuterRef, Subquery, Q,Sum
from pyfcm import FCMNotification
# import haversine as hs
# from haversine import Unit as Units
import json



status404 =status.HTTP_404_NOT_FOUND
status201 = status.HTTP_201_CREATED
_name = 1

def index(req):
    return render(req,'index.html')
def Today():
    return datetime.date(datetime.today())

def TokenAuth(user):
    check = Token.objects.filter(user=user[0].id)
    utype = UserDetails.objects.filter(username=user[0].id)
    if len(check)>0:                                                                    #----To check the user has alredy A TOKEN
        new_key = check[0].generate_key()                                               #-----
        check.update(key=new_key)                                                       #------- if a TOKEN Exists Update it
        result = {'msg':'success','token':new_key,'usertype':str(utype[0].usertype),'gender':utype[0].gender,'name':user[0].first_name,'last_name':user[0].last_name,'username':user[0].username,'email':user[0].email,'location':utype[0].location_id,'phone':utype[0].phone}
        return Response (result)
    else:
        token= Token.objects.create(user=user[0])                                       #-- ifname there is no old TOKEN, Genarate New TOKEN
        result = {'msg':'success','token':token.key,'usertype':str(utype[0].usertype),'gender':utype[0].gender,'name':user[0].first_name,'last_name':user[0].last_name,'username':user[0].username,'email':user[0].email ,'location':utype[0].location_id,'phone':utype[0].phone}
        return Response (result)

class ForgotPassword(APIView):
    def post(self,req):
        _user = User.objects.filter(username=req.data.get('username'))
        if _user:
            password = make_password(req.data.get('password'))
            details = {'password':password}
            _serializer = UserSerialier(_user[0],data = details, partial = True)
            if _serializer.is_valid():
                _serializer.save()
                return TokenAuth(_user)
            else:
                return Response(_serializer.errors)
        else:
            return Response({'msg':'fail'})

class Profile(APIView):
    def post(self,req):
        user =  User.objects.filter(username=req.data.get('username'))
        if user:
            utype = UserDetails.objects.filter(username=user[0].id)
            result = {'name':user[0].first_name,'username':req.data.get('username'),'phone':utype[0].phone,'gender':utype[0].gender}
            return Response (result)
        else :
            return Response({"error":"Error"},status404)

class Login(APIView):
    def post(self,req):
        user =  User.objects.filter(username=req.data.get('username'))          #---Get the user detailsbased on
        if user:
            if check_password(req.data.get('password'),user[0].password):
                if req.method == 'POST' and 'fcmtoken' in req.data:
                    _token =req.data['fcmtoken']            
                    tkn = {"token":_token}      
                    utype = UserDetails.objects.filter(username=user[0].id)  
                    serializer = UserDetailsSerializer(utype, data=tkn,partial=True)
                    if serializer.is_valid():
                        serializer.save()

                return TokenAuth(user)
            else:
                return Response({"msg":'fail'})
        else:
            return Response({"msg":'fail'})

class RegisterApi(APIView):
    def post(self, req):
        details = req.data
        _user = {'username':details['username'],'password':make_password(details['password']),'is_superuser':0,'first_name':details['name'],'last_name':'','email':'','is_staff':0,'is_active':1,'date_joined':datetime.today()}
        serializer = UserSerialier(data = _user)
        if serializer.is_valid():
            serializer.save()
            _userType='2'
            if 'usertype' in req.data:
                _userType = '1'
            user_details = {'username':serializer.data['id'],"name":req.data['name'],'phone':details['phone'],'gender':details['gender'],'location':details['location'],'usertype':_userType}
            details_serializer = DetailsSerialier(data = user_details)
            if details_serializer.is_valid():
                details_serializer.save()
                user_details = {'username':details['username'],"name":req.data['name'],'phone':details['phone'],'gender':details['gender'],'location':details['location'],'usertype':_userType}
                return Response(user_details)
            else:
                return Response(details_serializer.errors)
        else:
            return Response(serializer.errors)

class getUnits(APIView):
    def get(self, req):
        tbl_unit = Unit.objects.all()
        serializer = UnitSerialier(tbl_unit, many=True)
        return Response(serializer.data)

class GetCatagory(APIView):    #-------- Location Based Catagory Api--------#
    def post(self, req):
        loc = req.data['location']
        if loc is not None:
            tbl_catagory = Catagory.objects.filter(location=loc)
            serializer = CatagorySerializer(tbl_catagory, many=True)
            return Response(serializer.data)

## For Address return to MObile
class GetAddress(APIView):
    def post(self,req):
        uname = req.data['username']
        tbl_address = Address.objects.filter(username__username=uname)
        serializer = GetAddressSerializer(tbl_address,many=True)
        return Response(serializer.data)

class CatagoryApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, req, pk=None):
        if pk is not None:
            tbl_catagory = Catagory.objects.get(id=pk)
            serializer = CatagorySerializer(tbl_catagory)
            return Response(serializer.data)

        tbl_catagory = Catagory.objects.all()
        serializer = CatagorySerializer(tbl_catagory,many=True)
        return Response(serializer.data)

    def post(self, req):
        print(req.data)
        serializer = CatagorySerializer(data = req.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({'msg':1})
        else:
            return Response(serializer.errors)

    def put(self, req, pk):
        tbl_catagory = Catagory.objects.get(id=pk)
        serializer = CatagorySerializer(tbl_catagory, data = req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({'msg':1})
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        tbl_catagory = Catagory.objects.get(id=pk)
        if tbl_catagory.image:
            tbl_catagory.image.delete()
        tbl_catagory.delete()
        return Response({'msg':1})

#------ProductApi-----------#

class GetProducts(APIView):    #-------- Location Based Catagory Api--------#
    def get(self, req, loc=None):
        if loc is not None:
            tbl_product = Product.objects.filter(location=loc)
            serializer = ProductDetailsSerialier(tbl_product, many=True)
            return Response(serializer.data)
        else:
            return Response([])

    def post(self, req):
        loc = req.data['location']
        if  'category' in req.data :
            if loc is not None:
                tbl_catagory = Product.objects.filter(location=loc,catagory=req.data['category'])
                serializer = UserProductSerializer(tbl_catagory, many=True)
                return Response(serializer.data)
        elif 'featured' in req.data :
            if loc is not None:
                tbl_catagory = Product.objects.filter(location=loc,featured=True)
                serializer = UserProductSerializer(tbl_catagory, many=True)
                return Response(serializer.data)


class ProductApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, req, pk=None):
        if pk is not None:
            tbl_product = Product.objects.filter(id=pk)
            if tbl_product:
                serializer = ProductSerialier(tbl_product[0])
                return Response(serializer.data)
            else:
                return Response({'msg':0})
        tbl_product = Product.objects.all()
        serializer = ProductDetailsSerialier(tbl_product, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = ProductSerialier(data = req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':1})
        else:
            return Response(serializer.errors)

    def put(self, req, pk):
        tbl_product = Product.objects.get(id=pk)
        serializer = ProductSerialier(tbl_product, data = req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':1})
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        tbl_product = Product.objects.get(id=pk)
        if tbl_product.image:
            tbl_product.image.delete()
        tbl_product.delete()
        return Response({'msg':1})

class CatagoryNames(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(sel, req , loc =None):
        catagoris = Catagory.objects.filter(location=loc).values('id','name')
        return Response(list(catagoris))

class CatagoryBasedProducts(APIView):
    def post(self,req):
        tbl_product = Product.objects.filter(catagory=req.data.get('catagory'))
        serializer = SelectedProductserializer(tbl_product,many=True)
        return Response(serializer.data)

class ProductUpdate(APIView):      #----------Update All product Price-----------#
    def put(sel,req):
        productList =req.data
        for x in productList:
            tbl_product = Product.objects.get(id=x['id'])
            serializer = ProductSerialier(tbl_product, data = x, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({serializer.errors})
        return Response({"msg":1})

class AllDelivaryBoys(APIView): #---------GetThe Delivary Boys Details
    def get(self, req, loc):
        tbl_dboy = UserDetails.objects.filter(usertype=1, location=loc,username__is_active=True)
        serializer = UserDetailsSerializer(tbl_dboy, many=True)
        return Response(serializer.data)

class OneDelivaryBoys(APIView): #---------GetThe Delivary Boys Details
    def post(self, req):
        uname = req.data['username']
        tbl_dboy = UserDetails.objects.get(username__username=uname)
        serializer = UserDetailsSerializer(tbl_dboy)
        return Response(serializer.data)

class GetAllOrder(APIView):   #---------Based on Location--------#
    def get(self, req, loc):
        tbl_order = Order.objects.filter(location=loc,date__icontains=Today()).order_by('shipper')
        if tbl_order:
            serializer = AllOrderSerializer(tbl_order, many=True)
            return Response(serializer.data)
        else:
            return Response(tbl_order)



class OrderApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, req, pk=None):     #-----------Get The Order Details-----------#
        if pk is not None:
            tbl_order = Order.objects.filter(id=pk)
            if tbl_order:
                serializer = AllOrderSerializer(tbl_order[0])
                return Response(serializer.data)
            else:
                return Response({'msg':0})
        tbl_order = Order.objects.filter(date__icontains= datetime.date(datetime.today())).order_by('shipper')
        serializer = AllOrderSerializer(tbl_order, many=True)
        return Response(serializer.data)

    def post(self, req):
        orderdetails = req.data['orderdetails']                     #----Ordr Details Array-----#
        customer = req.data['customer']                             #------- Customer Details ----#
        tbl_user = User.objects.get(username= customer['username'])     #---------To get The id of username primry key table----(tbl_user.id)----#
        #-------Address Details --------#
        address = {'id':customer['address_id'],'name':customer['name'],'username':tbl_user.id, 'phone':customer['phone'], 'address':customer['deliveryaddress'], 'pin':customer['pincode'], 'landmark':customer['landmark'], 'latitude':customer['latitude'],'longitude':customer['longitude'],'geolocation':customer['geolocation']}
        # address = Address('username'tbl_user.id, 'phone':customer['phone'], 'address':customer['deliveryaddress'], 'pin':customer['pincode'], 'landmark':customer['landmark'], 'latitude':customer['latitude'],'longitude':customer['longitude'],'geolocation':customer['geolocation']}
        adrs_serializer = AddressSerializer(data= address)
        if adrs_serializer.is_valid():
            adrs_serializer.save()
            #------- Order table Values nsertion ---------#
            order = {'username': tbl_user.id, 'address': adrs_serializer.data['id'],'inv_number':random.randint(1000,9999),'total_amount':req.data['total_amount'],'payment_type':req.data['payment_type'],'status':1,'location':customer['geolocation'],"shiping_charge":req.data['shiping_charge']}

            order_serializer = OrderSerializer(data = order)
            if order_serializer.is_valid():
                order_serializer.save()
                for x in orderdetails:
                    #---------Order_Details values insertion-----#
                    details ={'order':order_serializer.data['id'], 'product': x['product'], 'quantity': x['qty'], 'amount': x['total'],'status':True }

                    Orderdetails_serializer = AddOrderDetailsSeializer(data = details)
                    if Orderdetails_serializer.is_valid():
                        Orderdetails_serializer.save()
                    else:
                        return Response({'msg':0,'errors':Orderdetails_serializer.errors})
                return Response({'msg':1})
            else:
                return Response({'msg':0,'errors':order_serializer.errors})
        else:
            return Response({'msg':0,'errors':adrs_serializer.errors})



    def put(self, req, pk):
        tbl_order = Order.objects.get(id=pk)
        serializer = OrderSerializer(tbl_order, data = req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':1})
        else:
            return Response(serializer.errors)


def CheckShipper(shipper):
    DelBoy = Shipper.objects.filter(delivary_boy=shipper)
    if DelBoy:
        return DelBoy[0].id
    else:
        serializer = ShipperSerializer(data={'delivary_boy':shipper})
        if serializer.is_valid():
            serializer.save()
            return serializer.data['id']
        else:
            print(serializer.errors)
            return False

class AssignOrders(APIView):
    def put(self, req):
        order = req.data.get('orders')
        shipper = req.data.get('shipper')
        id = CheckShipper(shipper)
        if id:
            for x in order:
                tbl_order = Order.objects.get(id=x)
                data= {'shipper':id,'status':2}
                order_serializer = OrderSerializer(tbl_order,data = data, partial=True)
                if order_serializer.is_valid():
                    order_serializer.save()
                else:
                    return Response({'msg':0,'errors':order_serializer.errors})
            return Response({'msg':1})
        else:
            return Response({'msg':0})

class FilterOrder(APIView):
    def post(self, req, loc):
        print(req.data)
        order = Order.objects.filter(date__icontains=req.data.get('date') ,status=req.data.get('status'),location=loc)
        order_serializer = AllOrderSerializer(order, many=True)
        return Response(order_serializer.data)

class OrderDetailsApi(APIView):
    def get(self, req, id):
        tbl_orderDetails = OrderDeatails.objects.filter(order=id)
        serializer = OrderDetailsSeializer(tbl_orderDetails, many=True)
        return Response(serializer.data)


class DashBoard(APIView):
    def get(self, req, loc):
        #--------- Count ----------#

        data = Order.objects.filter(location=loc).exclude(status__lt=1).\
            aggregate( total=Count('status',filter=Q(date__icontains=Today())),completed = Count('status',filter=Q(status=3,date__icontains=Today())),pending = Count('status',filter=Q(status__lte=2,status__gte=1)), amount =Sum('total_amount',filter=Q(status=3,date__icontains=Today())),shiping_charge =Sum('shiping_charge',filter=Q(status=3,date__icontains=Today())))

        #------------ Recent Order-------#
        last_order = Order.objects.filter(location=loc,status__gte=2).order_by('-id')[:10]
        order_serializer = AllOrderSerializer(last_order,many=True)

        total = 0
        if data['amount'] and data['shiping_charge']:
            total += data['amount']+ data['shiping_charge']
        elif data['amount']:
            total = data['amount']
        elif data['shiping_charge']:
            total = data['shiping_charge']

        return Response({'total_order':data['total'], 'completed':data['completed'], 'pending':data['pending'], 'total':total, 'order':order_serializer.data})


class DelvaryDashboard(APIView):
    def get(self, req, loc):
        data = Order.objects.filter(location=loc).exclude(status__lt=2).values('shipper__delivary_boy__first_name','shipper__delivary_boy__last_name').\
            annotate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)), amount =Sum('total_amount',filter=Q(status=3,payment_type=0))).exclude(shipper__isnull=True)[:10]
        serializer = DelivaryDashBoarSerilaizer(data, many=True)
        return Response(serializer.data)

class ProductReport(APIView):
    def post(self, req, loc):
        print(req.data)
        if req.data.get('start') and req.data.get('end') :
            if req.data.get('start') == req.data.get('end') :
                data = OrderDeatails.objects.filter(order__status=3,order__location=loc,order__date__icontains=req.data.get('start')).\
                    values('product__name','product__id','product__unit__unit').\
                    annotate(amount=Sum('amount'),qty_sum=Sum('quantity')).filter(product__catagory=req.data.get('catagory'))
            else:
                data = OrderDeatails.objects.filter(order__status=3,order__location=loc,order__date__gte=req.data.get('start'),order__date__lte=req.data.get('end')).\
                    values('product__name','product__id','product__unit__unit').\
                    annotate(amount=Sum('amount'),qty_sum=Sum('quantity')).filter(product__catagory=req.data.get('catagory'))
        else:                           #-------------------In casedate didnt -----------------------------------#
            data = OrderDeatails.objects.filter(order__status=3,order__location=loc).\
                values('product__name','product__id','product__unit__unit').\
                annotate(amount=Sum('amount'),qty_sum=Sum('quantity')).filter(product__catagory=req.data.get('catagory'))
        serializer = ProducaReportSerializer(data, many=True)
        return Response(serializer.data)


def AddressCheck(order):
    customer = order.get('customer')
    if  customer['address_id'] != None:
        _address = Address.objects.get(id=customer['address_id'])
        address = {'phone':customer['phone'], 'address':customer['deliveryaddress'],'name':customer['name'], 'pin':customer['pincode'], 'landmark':customer['landmark'], 'latitude':customer['latitude'],'longitude':customer['longitude'],'geolocation':customer['geolocation']}
        serializer = AddressSerializer(_address,data=address, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data['id']
        else:
            return serializer.errors
    else:
        tbl_user = User.objects.get(username=customer.get('username'))
        address = {'username':tbl_user.id,'phone':customer['phone'], 'name':customer['name'], 'address':customer['deliveryaddress'], 'pin':customer['pincode'], 'landmark':customer['landmark'], 'latitude':customer['latitude'],'longitude':customer['longitude'],'geolocation':customer['geolocation']}
        serializer = AddressSerializer(data=address)
        if serializer.is_valid():
            serializer.save()
            return serializer.data['id']
        else:
            return serializer.errors

class OrderPlace(APIView):
    def post(self, req):
        orderdetails = req.data['orderdetails']                     #----Ordr Details Array-----#
        customer = req.data['customer']                             #------- Customer Details ----#
        tbl_user = User.objects.get(username= customer['username'])     #---------To get The id of username primry key table----(tbl_user.id)----#
        address = AddressCheck(req.data)
        if type(address)==int:
            #------- Order table Values nsertion ---------#
            inv = random.randint(1000,9999)
            order = {'username': tbl_user.id, 'address': address,'inv_number':inv,'total_amount':req.data['total_amount'],'shiping_charge':req.data['shiping_charge'],'payment_type':req.data['payment_type'],'status':1,'location':req.data['location']}
            order_serializer = OrderSerializer(data = order)
            if order_serializer.is_valid():
                order_serializer.save()
                for x in orderdetails:
                    #---------Order_Details values insertion-----#
                    details ={'order':order_serializer.data['id'], 'product': x['product'], 'quantity': x['qty'], 'amount': x['total'],'status':True }

                    Orderdetails_serializer = AddOrderDetailsSeializer(data = details)
                    if Orderdetails_serializer.is_valid():
                        Orderdetails_serializer.save()
                    else:
                        return Response({'errors':Orderdetails_serializer.errors})
                order = {'username':customer['username'], 'address': "address",'inv_number':str(inv),'total_amount':req.data['total_amount'],'shiping_charge':req.data['shiping_charge'],'payment_type':req.data['payment_type'],'status':1,'location':req.data['location']}
                ########################################################
                push_service = FCMNotification(api_key="AAAAYCtex6w:APA91bH9x_KPTD0SzKrk3CauKNqWaI-UzgtJM49vsqkRoj0exQ0pxKLhXXHd2PVesQiDlpW_VlHqFch2c6ix-WPWoZhWb5IGKfRZNZ-z1TTZc7ZdiDiO3i1zFq6VryQv9Tt0dB529IjP")
                notifi_content = 'TCom Delivery '   
                
                _token=''
                if UserDetails.objects.filter(username= tbl_user.id).exists():
                    _token = UserDetails.objects.filter(username= tbl_user.id).first().token
                    message_title = 'TCom Delivery Order'                
                    message_body = 'Your Order  Placed Successfully .. We will be deliver as soon as possible ' #+ "\n "+ registration.akshya.name
                    #For Single Device Notification...
                    data = {"title":message_title,"body":message_body,"Room":"Track Akshaya"}
                    result = push_service.notify_single_device(registration_id=_token, message_title=message_title, message_body=message_body,data_message=data,extra_notification_kwargs={"click_action": "trackakshaya"})
                    print("hiiiiiii")
                    print(result)
                    ########################################################
                return Response(order)
            else:
                return Response({'errors':order_serializer.errors})
        else:
            return Response({"errors":address})

class UserOrder(APIView):
    def post(self,req):
        cart = Order.objects.filter(username__username=req.data.get('username'),status__gte=1)
        serializer = AllOrderSerializer(cart, many=True)
        return Response(serializer.data)

#---------------------------------- CART --------------------------------------#

class AddCart(APIView):
    def post(self, req):
        orderdetails = req.data['orderdetails']                     #----Cart Details Array-----#
        customer = req.data['customer']                             #------- Customer Details ----#
        tbl_user = User.objects.get(username= customer['name'])     #---------To get The id of username primry key table----(tbl_user.id)----#
        #------- Order table Values nsertion ---------#
        order = {'username': tbl_user.id,'total_amount':customer['total_amount'],'status':0,'location':customer['location']}
        order_serializer = OrderSerializer(data = order)
        if order_serializer.is_valid():
            order_serializer.save()
            for x in orderdetails:
                #---------Order_Details values insertion-----#
                details ={'order':order_serializer.data['id'], 'product': x['product'], 'quantity': x['qty'], 'amount': x['total'],'status':True }

                Orderdetails_serializer = AddOrderDetailsSeializer(data = details)
                if Orderdetails_serializer.is_valid():
                    Orderdetails_serializer.save()
                else:
                    return Response({'msg':"fail",'errors':Orderdetails_serializer.errors})
            return Response({'msg':"success"})
        else:
            return Response({'msg':"fail",'errors':order_serializer.errors})

class Cart(APIView):
    def post(self,req):
        cart = Order.objects.filter(username__username=req.data.get('username'),status=0)
        serializer = AllOrderSerializer(cart, many=True)
        return Response(serializer.data)
#  -------------Order Report --------------------------------------------------#

class OrderReport(APIView):
    def post(self, req, loc):
        if req.data.get('start') and req.data.get('end'):
            if req.data.get('start') == req.data.get('end'):
                report = Order.objects.filter(status=3,location=loc,date__icontains=req.data.get('start')).order_by('payment_type')
            else:
                report = Order.objects.filter(status=3,location=loc,date__gte=req.data.get('start'),date__lte=req.data.get('end')).order_by('payment_type')
            serializer = OrderReportSerializer(report , many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"Cannot use None as Date"})

#  -------------Delivary  Report --------------------------------------------------#
class DelvaryReport(APIView):
    def post(self, req, loc):
        if req.data.get('start') and req.data.get('end'):
            if req.data.get('start') == req.data.get('end'):
                data = Order.objects.filter(location=loc,date__icontains=req.data.get('start')).exclude(status__lt=3).values('shipper__delivary_boy__first_name','shipper__delivary_boy__last_name').\
                    annotate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)))
            else:
                 data = Order.objects.filter(location=loc,date__gte=req.data.get('start'),date__lte=req.data.get('end')).exclude(status__lt=3).values('shipper__delivary_boy__first_name','shipper__delivary_boy__last_name').\
                    annotate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)))
            serializer = DelivaryReportSerilaizer(data, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"Cannot use None as Date"})

 #  -------------Income  Report --------------------------------------------------#
class IncomeReport(APIView):
    def post(self, req, loc):
        print(req.data)
        if req.data.get('start') and req.data.get('end'):
            if req.data.get('start') == req.data.get('end'):
                data = Order.objects.filter(location=loc,date__icontains=req.data.get('start')).exclude(status__lt=2).\
                    aggregate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)),canceled = Count('shipper',filter=Q(status=4)),pending = Count('shipper',filter=Q(status=2)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)))
                # print(data)
            else:
                data = Order.objects.filter(location=loc,date__gte=req.data.get('start'),date__lte=req.data.get('end')).exclude(status__lt=2).\
                    aggregate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)),canceled = Count('shipper',filter=Q(status=4)),pending = Count('shipper',filter=Q(status=2)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)))
                print(data)
            serializer = IncomeReportSerilaizer(data)
            return Response([serializer.data])
        else:
            return Response({"error":"Cannot use None as Date"})
#---------------------------------------------------------------------------------------#
#                       Shipping charge Calculation
        # dis = hs.haversine(loc1,loc2,unit=Units.METERS)
#---------------------------------------------------------------------------------------#

class ShippingCharge(APIView):
    def post(self , req, loc):
        try:
            #tbl_location = Location.objects.get(id = loc)
            #_key ="gmKhGXTGiR5GeVnsDngYV83jTEtJZ"
            #_url = "https://api.distancematrix.ai/maps/api/distancematrix/json?origins={},{}&destinations={},{}&key={}".format(tbl_location.latitude,tbl_location.longitude,req.data.get('latitude'),req.data.get('longitude'),_key)
            #r = requests.get(_url)

            #result = json.loads(r.text)
            #rows = result['rows']
            #elements = rows[0]['elements'][0]
            #distance = elements['distance']['text']
            #dis = distance.split(" ")
            amount =0 #float(dis[0])*10
            if amount<10:
                amount = 10
            return Response({"amount":amount})
        except:
            return Response("error")

class IncomeReport(APIView):
    def post(self, req, loc):
        print(req.data)
        if req.data.get('start') and req.data.get('end'):
            data = Order.objects.filter(location=loc,date__gte=req.data.get('start'),date__lte=req.data.get('end')).exclude(status__lt=2).\
                aggregate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)),canceled = Count('shipper',filter=Q(status=4)),pending = Count('shipper',filter=Q(status=2)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)))
            print(data)
            serializer = IncomeReportSerilaizer(data)
            return Response([serializer.data])
        else:
            return Response({"error":"Cannot use None as Date"})

class FeaturedProduct(APIView):
    def get(self, req, loc):
        _product = Product.objects.filter(featured=True,location=loc)
        serializer = ProductDetailsSerialier(_product,many=True)
        return Response(serializer.data)

class GetNoice(APIView):    #-------- Location Based Catagory Api--------#
    def get(self, req, loc=None):
        if loc is not None:
            _notice = Notice.objects.filter(location=loc,is_delete=False).order_by('-id')
            serializer = NoticeSerializer(_notice, many=True)
            return Response(serializer.data)


class NoticeApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, req, pk=None):
        if pk is not None:
            _notice = Notice.objects.filter(id=pk)
            if _notice:
                serializer = NoticeSerializer(_notice[0])
                return Response(serializer.data)
            else:
                return Response({'msg':0})
        _notice = Notice.objects.all()
        serializer = NoticeSerializer(_notice, many=True)
        return Response(serializer.data)

    def post(self, req):
        _user = User.objects.get(username=req.data.get('username'))
        if _user:
            req.data['username'] = _user.id
            serializer = NoticeSerializer(data = req.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':1})
            else:
                return Response(serializer.errors)
        else:
            return Response({"msg":0})

    def put(self, req, pk):
        _notice = Notice.objects.get(id=pk)
        serializer = NoticeSerializer(_notice, data = req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':1})
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        _notice = Notice.objects.get(id=pk)
        _notice.delete()
        return Response({'msg':1})

#----------------Banner Api-----------------------------#
class getBanner(APIView):
    def get(self, req, loc):
        _banner = Banner.objects.filter(location=loc)
        serializer = BannerSerializer(_banner, many=True)
        return Response(serializer.data)


class BannerApi(APIView):
    # permission_classes = (IsAuthenticated,)
    counter = 1
    def get(self, req, pk=None):
        if pk is not None:
            _banner = Banner.objects.filter(id=pk)
            if _banner:
                serializer = BannerSerializer(_banner[0])
                return Response(serializer.data)
            else:
                return Response({'msg':"fail"})
        _banner = Banner.objects.all()
        serializer = BannerSerializer(_banner, many=True)
        return Response(serializer.data)

    def post(self, req):
        print(req.data['image'])
        req.data['image'].name = "{}.jpg".format(BannerApi.counter)
        serializer = BannerSerializer(data = req.data)
        if serializer.is_valid():
            serializer.save()
            BannerApi.counter += 1
            return Response({'msg':"success"})
        else:
            return Response(serializer.errors)

    def put(self, req, pk):
        _banner = Banner.objects.get(id=pk)
        serializer = BannerSerializer(_banner, data = req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"success"})
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        _banner = Banner.objects.get(id=pk)
        if _banner.image:
            _banner.image.delete()
        _banner.delete()
        return Response({'msg':"success"})

# class RegisterApi(APIView):
#     def post(self, req):
#         details = req.data
#         _user = {'username':details['username'],'password':make_password(details['password']),'is_superuser':0,'first_name':details['name'],'last_name':'','email':'','is_staff':0,'is_active':1,'date_joined':datetime.today()}
#         serializer = UserSerialier(data = _user)
#         if serializer.is_valid():
#             serializer.save()
#             user_details = {'username':serializer.data['id'],'phone':details['phone'],'gender':details['gender'],'location':details['location'],'usertype':2}
#             details_serializer = DetailsSerialier(data = user_details)
#             if details_serializer.is_valid():
#                 details_serializer.save()
#                 user =  User.objects.filter(username=details['username'])
#                 return TokenAuth(user)
#             else:
#                 return Response(details_serializer.errors)
#         else:
#             return Response(serializer.errors)

# class Profile(APIView):
#     def post(self, req):
#         _userDetails = UserDetails.objects.get(username__username=req.data.get('username'))
#         serializer = UserDetailsSerializer(_userDetails)
#         return Response(serializer.data)

class UserAddress(APIView):
    def post(self, req):
        _address = Address.objects.filter(username__username=req.data.get('username'))
        serializer = GetAddressSerializer(_address, many=True)
        return Response(serializer.data)

#---------------------Delvary Boys Section---------------------------------------------#

class DelivaryBoysOrders(APIView):
    def post(self, req):
        _orders = Order.objects.filter(shipper__delivary_boy__username=req.data.get('username'),status=2).order_by('-date')
        serializer = DelivaryBoysOrderSerializer(_orders, many=True)
        return Response(serializer.data)

class DelivaryHistory(APIView):
    def post(self, req):
        _orders = Order.objects.filter(shipper__delivary_boy__username=req.data.get('username'),status__gte=3).order_by('-date')
        serializer = DelivaryBoysOrderSerializer(_orders, many=True)
        return Response(serializer.data)

class UpdateOrderStatus(APIView):
    def post(self, req):
        _order = Order.objects.get(id = req.data.get('id'))
        if req.data.get('status') == 3 :
            details = {'delivary_remarks':req.data.get('summery'),'status':req.data.get('status'),'delivary_date':datetime.now(),'payment_status':1}
        else:
            details = {'delivary_remarks':req.data.get('summery'),'status':req.data.get('status'),'delivary_date':datetime.now()}
        serializer = OrderSerializer(_order,data = details,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"success"})
        else:
            return Response({"msg":serializer.errors})

    def put(self,req): #----For Updating delivery boys Status / used to activate or Deactivate DeliveryBoys------#
        _user = User.objects.get(id=req.data.get('id'))
        # status = {'is_active':req.data.get('status')}
        _serializer = UserSerialier(_user,req.data, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response({"msg":"success"})
        else:
            return Response(_serializer.errors)

#----------------------LOCATION API------------------#

class LocationApi(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, req, pk=None):
        if pk is not None:
            _location = Location.objects.get(id=pk)
            serializer = LocationSerializer(_location)
            return Response(serializer.data)

        _location = Location.objects.all()
        serializer = LocationSerializer(_location,many=True)
        return Response(serializer.data)

    def post(self, req):
        print(req.data)
        serializer = LocationSerializer(data = req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"success"})
        else:
            return Response(serializer.errors)

    def put(self, req, pk):
        _location = Location.objects.get(id=pk)
        serializer = LocationSerializer(_location, data = req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"success"})
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        _location = Location.objects.get(id=pk)
        if _location.qr_code:
            _location.qr_code.delete()
        _location.delete()
        return Response({'msg':"success"})

#-------------------Reset Password --------------------------#

class ResetPassword(APIView):
    def post(self, req):
        _user = User.objects.filter(username=req.data.get('username'))
        if _user:
            if check_password(req.data.get('password'),_user[0].password):
                data = {'password':make_password(req.data.get('newpass'))}
                _serializer = UserSerialier(_user[0],data, partial=True)
                if _serializer.is_valid():
                    _serializer.save()
                    return Response({'msg':'success'})
                else:
                    return Response(_serializer.errors)
            else:
                return Response({'msg':'fail'})
        else:
            return Response({'msg':'fail'})

#-----FILTER ORDER---#
class FilterOrder(APIView):
    def post(self, req, loc):
        # print(req.data)
        if req.data['status']=='5':
            order = Order.objects.filter(status__gt=0,status__lt=3,location=loc).order_by('status')
        else:
            order = Order.objects.filter(date__icontains=req.data.get('date') ,status=req.data.get('status'),location=loc)
        order_serializer = AllOrderSerializer(order, many=True)
        return Response(order_serializer.data)

#------ALL Delivery Boys DEtails----#

class AllDelivaryBoys(APIView): #---------GetThe Delivary Boys Details
    def post(self, req):
        if req.data.get('status'):
            tbl_dboy = UserDetails.objects.filter(usertype=1, location=req.data.get('location'),username__is_active=req.data.get('status'))
        else:
            tbl_dboy = UserDetails.objects.filter(usertype=1, location=req.data.get('location'))
        serializer = UserDetailsSerializer(tbl_dboy, many=True)
        return Response(serializer.data)

class AllIncomeReport(APIView):
    def post(self, req):
        print(req.data)
        if req.data.get('start') and req.data.get('end'):
            if req.data.get('start') == req.data.get('end'):
                data = Order.objects.filter(date__icontains=req.data.get('start')).values('location__name').exclude(status__lt=2).\
                    annotate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)),canceled = Count('shipper',filter=Q(status=4)),pending = Count('shipper',filter=Q(status=2)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)))
                # print(data)
            else:
                data = Order.objects.filter(date__gte=req.data.get('start'),date__lte=req.data.get('end')).values('location__name').exclude(status__lt=2).\
                    annotate( total=Count('shipper'),completed = Count('shipper',filter=Q(status=3)),canceled = Count('shipper',filter=Q(status=4)),pending = Count('shipper',filter=Q(status=2)), cod_amount =Sum('total_amount',filter=Q(status=3,payment_type=0)), upi_amount =Sum('total_amount',filter=Q(status=3,payment_type=1)),shiping_charge =Sum('shiping_charge',filter=Q(status=3)))
                print(data)
            serializer = AllIncomeReportSerilaizer(data, many=True)
            return Response(serializer.data)
        else:
            return Response({"error":"Cannot use None as Date"})


#-------------- ALL ADMIN ------------#

class AllAdmin(APIView):
    def get(self, req):
        _admin = UserDetails.objects.filter(usertype=0)
        serializer = UserDetailsSerializer(_admin, many=True)
        return Response(serializer.data)

    def post(self, req):
        _user = UserDetails.objects.get(username=req.data.get('id'))
        data = {'usertype':2}
        _serializer = DetailsSerialier(_user,data, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response({'msg':"success"})
        else:
            return Response(_serializer.errors)

#-------------- ALL ADMIN ------------#

class AllAdmin(APIView):
    def get(self, req):
        _admin = UserDetails.objects.filter(usertype=0)
        serializer = UserDetailsSerializer(_admin, many=True)
        return Response(serializer.data)

    def post(self, req):
        _user = UserDetails.objects.get(username=req.data.get('id'))
        data = {'usertype':2}
        _serializer = DetailsSerialier(_user,data, partial=True)
        if _serializer.is_valid():
            _serializer.save()
            return Response({'msg':"success"})
        else:
            return Response(_serializer.errors)

