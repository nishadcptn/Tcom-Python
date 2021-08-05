from django.db import models
from django.contrib.auth.models import User
# from django_dropbox_storage.storage import DropboxStorage

# DROPBOX_STORAGE = DropboxStorage()


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField( max_length=10)
    latitude = models.DecimalField( max_digits=22, decimal_places=16,null = True, blank=True)
    longitude =models.DecimalField( max_digits=22, decimal_places=16,null = True, blank=True)
    upi_number = models.CharField( max_length=10,null = True, blank=True)
    qr_code = models.ImageField( upload_to="location/",null = True, default = None,blank=True)
    class Meta:
        db_table = "Location"

    def __str__(self):
        return self.name

class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField( upload_to="banner/")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField()
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "Banner"


class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.CharField( max_length=50)
    class Meta:
        db_table = "Unit"
    def __str__(self):
        return self.unit

class Catagory(models.Model):               #----Catagory Details----#
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=50)
    description = models.TextField(null = True, default = None,blank=True)
    status = models.BooleanField(default=True)
    image = models.ImageField( upload_to="catagory/",null = True, default = None,blank=True)
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "Catagory"


class Company(models.Model):            #-----Company details---------#
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=50)
    address = models.TextField()
    pin = models.IntegerField()
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    logo = models.ImageField(upload_to="Company/")
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "Company"

class Product(models.Model):            #---------Product details-------#
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=50)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    description = models.TextField(null = True, default = None,blank=True)
    price = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null = True, default = None,blank=True)
    size = models.IntegerField(null = True, default = None,blank=True)
    color = models.CharField(max_length=50,null = True, default = None,blank=True)
    image = models.ImageField(upload_to="Product/",null = True, default = None,blank=True)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    discount = models.FloatField(default=None,null=True,blank=True)
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "Product"

class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Product_image/")
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = "ProductImage"

class UserDetails(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    gender = models.CharField(max_length=20)
    usertype = models.IntegerField()  #--0 /Admin---1/Deliv_boy ----2/user
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    token=models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        db_table = "UserDetails"


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User ,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,default=None)
    phone = models.CharField(max_length=10)
    email = models.EmailField( max_length=254,null=True,blank=True,default=None)
    address = models.TextField()
    pin =  models.IntegerField()
    landmark = models.CharField( max_length=50)
    latitude = models.DecimalField( max_digits=22, decimal_places=16)
    longitude =models.DecimalField( max_digits=22, decimal_places=16)
    # type = models.CharField( max_length=50)
    geolocation = models.CharField( max_length=50,default=None,null=True,blank=True)
    is_delete = models.BooleanField(default=False)
    class Meta:
        db_table = "Address"

class ShippingCharge(models.Model):            #----- not in use
    id = models.AutoField(primary_key=True)
    total_amount = models.FloatField()
    min_ship_amount = models.FloatField()
    class Meta:
        db_table = "ShippingCharge"

class Payment(models.Model):              #----- not in use
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)      #-------Payment Type
    shipping = models.ForeignKey(ShippingCharge, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    class Meta:
        db_table = "Payment"

class Shipper(models.Model):
    id = models.AutoField(primary_key=True)
    delivary_boy = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "Shipper"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)    #  null=True,blank=True,default=None --- For Adding cart
    date = models.DateTimeField( auto_now=True)
    delivary_date = models.DateTimeField(null=True,blank=True,default=None)
    payment_type = models.IntegerField()      #-------Payment Type 0 / COD 1/ UPI
    status = models.IntegerField(default=0)  # -------/0- default / 1- Order Placed/ 2-shiped/ 3- completed/4- cancel Order
    payment_status = models.BooleanField(default=False)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE,null=True,blank=True,default=None)
    inv_number = models.IntegerField()  #--------Invoice Number
    total_amount = models.FloatField()
    shiping_charge =  models.FloatField()
    delivary_remarks = models.TextField(null=True,blank=True,default=None)
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "Order"

class OrderDeatails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField( auto_now=True)
    quantity = models.IntegerField()
    amount = models.FloatField()
    status = models.BooleanField(default=False)
    class Meta:
        db_table = "OrderDeatails"


class Whishlist(models.Model):
    id =models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    class Meta:
        db_table = "Whishlist"

class Offers(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_price = models.FloatField()
    Description = models.TextField()
    date = models.DateTimeField()
    last_date = models.DateTimeField()
    class Meta:
        db_table = "Offers"

class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    condent = models.TextField()
    date = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    location = models.ForeignKey(Location ,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "Notice"

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    condent = models.TextField()
    date = models.DateTimeField(auto_now=False)
    class Meta:
        db_table = "Review"