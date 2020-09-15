from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import category, subcategory, products
import json


# Create your views here.


def home(request):
    return render(request, 'base.html')


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return str(obj)
        return super().default(obj)


@csrf_exempt
def addproduct(request):
    formdata = json.loads(request.body.decode('utf-8'))
    print(formdata['categoryId'])
    prd = products(
        cat_name=category.objects.get(pk=formdata['categoryId']),
        subCat_id=subcategory.objects.get(pk=formdata['subCategoryId']),
        official_name=formdata['name'],
        type_name=formdata['type'],
        buy_price=formdata['buyPrice'],
        sell_price=formdata['sellPrice']
    )
    prd.save()
    return JsonResponse([{"hello": "world"}], safe=False)


def getlist(request):
    product_objects = products.objects.all()
    arr = []
    for product in product_objects:
        print(product.cat_name)
        result = {
            "id": product.pk,
            "name": product.official_name,
            "type": product.type_name,
            "buyPrice": product.buy_price,
            "sellPrice": product.sell_price,
            "catTitle": product.cat_name.cat_name,
            "subCatTitle": product.subCat_id.subCat_name
        }
        arr.append(result)
    return JsonResponse(arr, safe=False)


def getcategorylist(request):
    category_objects = category.objects.all()
    arr = []
    for cat in category_objects:
        arr.append({
            "name": cat.cat_name,
            "id": cat.pk
        })

    return JsonResponse(arr, safe=False)


@csrf_exempt
def getsubcategorylist(request):
    data = json.loads(request.body.decode('utf-8'))
    subcategory_objects = subcategory.objects.all()
    print(subcategory_objects)
    arrr = []
    for subcat in subcategory_objects:
        if subcat.cat_id.pk == data['id']:
            arrr.append({
                "id": subcat.pk,
                "catId": subcat.cat_id.pk,
                "name": subcat.subCat_name
            })

    return JsonResponse(arrr, safe=False)


@csrf_exempt
def deleteproduct(request):
    data = json.loads(request.body.decode('utf-8'))
    prd = products.objects.get(pk=data['id'])
    prd.delete()
    return JsonResponse({"msg": 'deleted'}, safe=False)
