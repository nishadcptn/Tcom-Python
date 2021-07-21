"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from App.views import *
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',Login.as_view(), name='LoinApi'),
    path('profile/',Profile.as_view(), name='ProfileApi'),
    path('register/',RegisterApi.as_view(), name='Register'),

    path('unit/',getUnits.as_view(), name='UnitList'),

    path('catagory/',CatagoryApi.as_view(), name='CatagoryApi'),
    path('catagory/<int:pk>',CatagoryApi.as_view(), name='CatagoryApiUpdate'),
    path('getcatagories/',GetCatagory.as_view(), name='GetCatagory'),     #--------- Location Based Catagory-----#

    path('notice/',NoticeApi.as_view(), name='NoticeApi'),
    path('notice/<int:pk>',NoticeApi.as_view(), name='NoticeApi'),
    path('notices/<int:loc>',GetNoice.as_view(), name='GetNoticeApi'),     #--------- Location Based Notice-----#

    path('product/',ProductApi.as_view(), name='ProductApi'),
    path('product/<int:pk>',ProductApi.as_view(), name='ProductApiUpdate'),
    path('getproducts/',GetProducts.as_view(), name='GetProducts'),        #--------- Location Based Products-----#
    path('getproducts/<int:loc>',GetProducts.as_view(), name='GetProducts'),        #--------- Location Based Products-----#
    path('featuredproducts/<int:loc>',FeaturedProduct.as_view(), name='FeaturedProduct'),        #--------- Location Based Products-----#

    path('selectedproduct/',CatagoryBasedProducts.as_view(), name='SelectedProductApiUpdate'),
    path('updateproduct/',ProductUpdate.as_view(), name='updateproduct'),

    path('catagorylist/<int:loc>',CatagoryNames.as_view(), name='CatagoryList'),        #-----Location Based Catagory list ---#
    path('delivaryboys/<int:loc>',AllDelivaryBoys.as_view(), name='AllDelivaryBoys'),
    path('delivaryboys/',AllDelivaryBoys.as_view(), name='AllDelivaryBoys'),
    path('delivaryboy/',OneDelivaryBoys.as_view(), name='OneDelivaryBoys'),

    path('getaddress/',GetAddress.as_view(), name='getAddress'),

    path('order/',OrderApi.as_view(), name='OrderApi'),
    path('order/<int:pk>',OrderApi.as_view(), name='OrderApiSpecific'),

    path('orders/<int:loc>',GetAllOrder.as_view(), name='OrderApi'),
    path('assignorders/',AssignOrders.as_view(), name='AssignOrder'),

    path('filterOrder/<int:loc>',FilterOrder.as_view(),name ='FilterOrder'),
    path('orderdetails/<int:id>',OrderDetailsApi.as_view(),name ='OrderDetailsApi'),
    path('dashboard/<int:loc>',DashBoard.as_view(),name ='DashBoard'),
    path('delreport/<int:loc>',DelvaryDashboard.as_view(),name ='DashBoard'),
    path('productreport/<int:loc>',ProductReport.as_view(), name="ProductReport"),

    path('orderreport/<int:loc>',OrderReport.as_view(), name='OrderReport'),
    path('delivaryreport/<int:loc>',DelvaryReport.as_view(), name='DelvaryReport'),
    path('incomereport/<int:loc>',IncomeReport.as_view(), name='IncomeReport'),

    path('getbanner/<int:loc>',getBanner.as_view(), name='getBanner'),
    path('banner/',BannerApi.as_view(), name='BannerApi'),
    path('banner/<int:pk>',BannerApi.as_view(), name='BannerApi'),

    path('orderplace/',OrderPlace.as_view(), name='OrderPlace'),
    path('userorder/',UserOrder.as_view(), name='UserOrder'),

    path('addcart/',AddCart.as_view(), name='AddCart'),
    path('usercart/',Cart.as_view(), name='UserCart'),

    path('getorders/',DelivaryBoysOrders.as_view(), name='DelivaryBoysOrders'),
    path('getorderhistory/',DelivaryHistory.as_view(), name='DelivaryHistory'),
    path('updatestatus/',UpdateOrderStatus.as_view(), name='UpdateOrderStatus'),
    path('shippingcharge/<int:loc>',ShippingCharge.as_view(), name='ShippingCharge'),
    path('resetpassword/',ResetPassword.as_view(), name='ResetPassword'),
    path('location/',LocationApi.as_view(), name='Location'),
    path('location/<int:pk>',LocationApi.as_view(), name='Location'),

    path('allincomereport/',AllIncomeReport.as_view(), name='AllIncomeReport'),
    path('alladmin/',AllAdmin.as_view(), name='AllAdmin'),
    path('forgotpwd/',ForgotPassword.as_view(), name='ForgotPassword'),
    url(r'^$', index)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
