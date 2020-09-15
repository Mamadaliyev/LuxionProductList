from django.contrib import admin
from .models import category, subcategory, products
# Register your models here.

admin.site.register([category, subcategory, products])
