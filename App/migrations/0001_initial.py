# Generated by Django 3.1.7 on 2021-07-19 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('address', models.TextField()),
                ('pin', models.IntegerField()),
                ('landmark', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('longitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('geolocation', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('status', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='catagory/')),
            ],
            options={
                'db_table': 'Catagory',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('upi_number', models.CharField(blank=True, max_length=10, null=True)),
                ('qr_code', models.ImageField(blank=True, default=None, null=True, upload_to='location/')),
            ],
            options={
                'db_table': 'Location',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('delivary_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('payment_type', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
                ('payment_status', models.BooleanField(default=False)),
                ('inv_number', models.IntegerField()),
                ('total_amount', models.FloatField()),
                ('shiping_charge', models.FloatField()),
                ('delivary_remarks', models.TextField(blank=True, default=None, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.address')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location')),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('price', models.FloatField()),
                ('size', models.IntegerField(blank=True, default=None, null=True)),
                ('color', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='Product/')),
                ('status', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('discount', models.FloatField(blank=True, default=None, null=True)),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.catagory')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ShippingCharge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.FloatField()),
                ('min_ship_amount', models.FloatField()),
            ],
            options={
                'db_table': 'ShippingCharge',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unit', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Unit',
            },
        ),
        migrations.CreateModel(
            name='Whishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.product')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Whishlist',
            },
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=12)),
                ('gender', models.CharField(max_length=20)),
                ('usertype', models.IntegerField()),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserDetails',
            },
        ),
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('delivary_boy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Shipper',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('condent', models.TextField()),
                ('date', models.DateTimeField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='Product_image/')),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.product')),
            ],
            options={
                'db_table': 'ProductImage',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.unit'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('shipping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.shippingcharge')),
            ],
            options={
                'db_table': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='OrderDeatails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('amount', models.FloatField()),
                ('status', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.product')),
            ],
            options={
                'db_table': 'OrderDeatails',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='shipper',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.shipper'),
        ),
        migrations.AddField(
            model_name='order',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('offer_price', models.FloatField()),
                ('Description', models.TextField()),
                ('date', models.DateTimeField()),
                ('last_date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.product')),
            ],
            options={
                'db_table': 'Offers',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('condent', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Notice',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('pin', models.IntegerField()),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('logo', models.ImageField(upload_to='Company/')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location')),
            ],
            options={
                'db_table': 'Company',
            },
        ),
        migrations.AddField(
            model_name='catagory',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location'),
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='banner/')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField()),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.location')),
            ],
            options={
                'db_table': 'Banner',
            },
        ),
    ]
