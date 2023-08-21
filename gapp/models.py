from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    CAT=((1,'VEGITABLE'),(2,'RICE'),(3,'Diary'))#this for if u want to give name to id for filter when u want to add any product  its very necessary ok then go to cat and give parameter choices=CAT OK THEN ITS WILL BE APPLIED OK
    name=models.CharField(max_length=100,verbose_name='product name')
    price=models.FloatField()
    pdetails=models.CharField(max_length=100,verbose_name='product details')
    cat=models.IntegerField(verbose_name='category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='available')
    pimage=models.ImageField(upload_to='image')#this is for add image to thire particular product name 

    



    def __str__(self): #this method it should be in class indended ok means class chya attmadhi
        return self.name
       
    


class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)



class Order(models.Model):
    order_id=models.CharField(max_length=98)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)



class contactrecords(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.CharField(max_length=20, default='')
    email=models.EmailField()    
    message=models.CharField(max_length=300)

