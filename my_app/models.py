from django.db import models
import json


# Create your models here.


class category(models.Model):
    cat_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cat_name



class subcategory(models.Model):
    cat_id = models.ForeignKey(category, on_delete=models.CASCADE)
    subCat_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subCat_name


class products(models.Model):
    cat_name = models.ForeignKey(category, on_delete=models.CASCADE)
    subCat_id = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    official_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    type_name = models.CharField(max_length=200)
    buy_price = models.DecimalField(decimal_places=0, max_digits=12)
    sell_price = models.DecimalField(decimal_places=0, max_digits=12)

    def __str__(self):
        return self.official_name
