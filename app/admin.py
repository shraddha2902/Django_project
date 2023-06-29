from django.contrib import admin
from app.models import Product,Order,Order_History


# Register your models here.
#define ModelAdminClass
class ProductAdminClass(admin.ModelAdmin):
    list_display=['name','cat','price','status']
    list_filter=['cat','status']

admin.site.register(Product,ProductAdminClass)
admin.site.site_header="Home Decor Dashboard"
admin.site.register(Order)
admin.site.register(Order_History)

