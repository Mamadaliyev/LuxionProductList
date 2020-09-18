from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import category, subcategory, products
import json
import xlwt

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
    prd = products(
        cat_name=category.objects.get(pk=formdata['categoryId']),
        subCat_id=subcategory.objects.get(pk=formdata['subCategoryId']),
        official_name=formdata['name'],
        type_name=formdata['type'],
        buy_price=formdata['buyPrice'],
        sell_price=formdata['sellPrice'],
        brand=formdata['brand']
    )
    prd.save()
    return JsonResponse([{"hello": "world"}], safe=False)


def getlist(request):
    product_objects = products.objects.all()
    arr = []
    for product in product_objects:
        result = {
            "id": product.pk,
            "name": product.official_name,
            "type": product.type_name,
            "buyPrice": product.buy_price,
            "sellPrice": product.sell_price,
            "catTitle": product.cat_name.cat_name,
            "subCatTitle": product.subCat_id.subCat_name,
            "brand": product.brand
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


@csrf_exempt
def getproductinfo(request):
    data = json.loads(request.body.decode('utf-8'))
    prd = products.objects.get(pk=data['id'])
    result = {
        "id": prd.pk,
        "name": prd.official_name,
        "type": prd.type_name,
        "buyPrice": prd.buy_price,
        "sellPrice": prd.sell_price,
        "catTitle": prd.cat_name.cat_name,
        "subCatTitle": prd.subCat_id.subCat_name,
        "categoryId": prd.cat_name.pk,
        "subCategoryId": prd.subCat_id.pk,
        "brand": prd.brand
    }
    return JsonResponse(result, safe=False)


@csrf_exempt
def updateproduct(request):
    formdata = json.loads(request.body.decode('utf-8'))
    prd = products.objects.get(pk=formdata['id'])
    prd.cat_name = category.objects.get(pk=formdata['categoryId'])
    prd.subCat_id = subcategory.objects.get(pk=formdata['subCategoryId'])
    prd.official_name = formdata['name']
    prd.type_name = formdata['type']
    prd.buy_price = formdata['buyPrice']
    prd.sell_price = formdata['sellPrice']
    prd.brand = formdata['brand']
    prd.save()
    return JsonResponse({"msg": "Product updated"}, safe=False)

@csrf_exempt
def export_all_products(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Products')

    row_num = 0
    first_col = ws.col(1)
    first_col.width = 350 * 20
    second_col = ws.col(2)
    second_col.width = 300 * 20
    seventh_col = ws.col(3)
    seventh_col.width = 220*20
    third_col = ws.col(4)
    third_col.width = 220 * 20
    fourth_col = ws.col(5)
    fourth_col.width = 220 * 20
    fifth_col = ws.col(6)
    fifth_col.width = 220*20
    sixth_col = ws.col(7)
    sixth_col.width = 220*20
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#', 'Категория', 'Подкатегория', 'Бренд', 'Название', 'Тип', 'Цена покупки', 'Цена продажи']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = products.objects.all()
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row_num, font_style)
        ws.write(row_num, 1, row.cat_name.cat_name, font_style)
        ws.write(row_num, 2, row.subCat_id.subCat_name, font_style)
        ws.write(row_num, 3, row.brand, font_style)
        ws.write(row_num, 4, row.official_name, font_style)
        ws.write(row_num, 5, row.type_name, font_style)
        ws.write(row_num, 6, row.buy_price, font_style)
        ws.write(row_num, 7, row.sell_price, font_style)
    wb.save(response)
    return response

