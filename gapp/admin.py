from django.contrib import admin
from gapp.models import Product

# Register your models here.

#admin.site.register(Product) # this is add ur product model into admin panel for admin access

#to do customisation in admin panel

#=======================================

#jar tumhala tumchi sarva model detail display karyachi asel admin panel var tar tumhala he karav lagel
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','is_active']
    list_filter=['cat','is_active']


admin.site.register(Product,ProductAdmin)

#=========================================



