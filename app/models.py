from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    CAT=((1,'furniture'),(2,'Kichen and Dining'),(3,'Wall Decor'))
    name=models.CharField(max_length=50,verbose_name='Product Name')
    cat=models.IntegerField(verbose_name='category',choices=CAT)
    price=models.FloatField()
    status=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image')



def __str__(self):
    return self.name

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.IntegerField()
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    qty=models.IntegerField()

    def __str__(self):
        return self.order_id

class Order_History(models.Model):
    order_id=models.CharField(max_length=400)
    pay_id=models.CharField(max_length=400)
    sign=models.CharField(max_length=400)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')

    def __str__(self):
        return self.order_id
    
class Profile(models.Model):
    uid=models.OneToOneField(User,on_delete=models.CASCADE,db_column='uid')
    mobile=models.CharField(unique=True,max_length=50)
    is_mobile_verified=models.BooleanField(default=False)
    is_gmail_verified=models.BooleanField(default=False)
    mobileotp=models.CharField(max_length=100,default=False)
    gmailotp=models.CharField(max_length=100,default=False)