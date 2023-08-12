from django.db import models
import datetime
from home.models import person

class food_category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class item(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(food_category , on_delete=models.CASCADE)
    price = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class order(models.Model):
    user = models.ForeignKey(person, null=True, on_delete=models.SET_NULL)
    total = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)


class orderitem(models.Model):
    item = models.ForeignKey(item, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(order, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)



'''
class alumni(models.Model):
    name = models.CharField(max_length=40)
    father = models.CharField(max_length=40)
    e_num = models.CharField(max_length=10, blank=True, null=True )
    image = models.FileField(upload_to='alumni/' , blank=True, null=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)
    address1 = models.TextField()
    address2 = models.TextField()
    from1 = models.TextField()
    upto1 = models.TextField()
    job = models.TextField()

    def __str__(self):
        return self.name



class gallery_type(models.Model):
    name = models.CharField(max_length=  40)
    description = models.TextField(blank=True)
    type_image = models.FileField(upload_to='gallery/' , blank=True, null=True)

    def __str__(self):
        return self.name



class gallery (models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(gallery_type , on_delete=models.CASCADE)
    dated_on = models.DateField(default=datetime.date.today)
    image = models.FileField(upload_to='gallery/' , blank=True, null=True)

    def __str__(self):
        return self.name


class article (models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=40)
    author_post = models.CharField(max_length=40)
    dated_on = models.DateField(default=datetime.date.today)
    image = models.FileField(upload_to='article/' , blank=True, null=True)

    def __str__(self):
        return self.title



class news(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    date = models.DateField(default=datetime.date.today)
    news_image = models.FileField(upload_to='news/')
    news_file = models.FileField(upload_to='news/', blank=True)

    def __str__(self):
        return self.title
'''