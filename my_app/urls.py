from django.urls import path

from . import views

app_name = 'my_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('addproduct/', views.addproduct, name='add_item'),
    path('getlist/', views.getlist, name='getlist'),
    path('getcategorylist/', views.getcategorylist, name='getcategorylist'),
    path('getsubcategorylist/', views.getsubcategorylist, name='getsubcategorylist'),
    path('deleteproduct/', views.deleteproduct, name='deleteproduct'),
    path('getproductinfo/', views.getproductinfo, name='getproductinfo'),
    path('updateproduct/', views.updateproduct, name='updateproduct'),
    path('export/xls/', views.export_all_products, name='export_all_products'),
]