from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
from . import PoolDict
import uuid
import os


def FinalProductInterface(request):
    try:
        result = request.session['ADMIN']
        return render(request, "FinalProductInterface.html")
    except Exception as e:
        return render(request, 'AdminLogin.html')

def DisplayFinalProductByIdJSON(request):
    finalproductid = request.GET['finalproductid']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid), (select P.productname from products P where P.productid = FP.productid) from finalproducts FP where finalproductid = {}".format(finalproductid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return JsonResponse(row, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def DisplayUpdatedStock(request):
    return render(request, "ListProductsEmployee.html")


def DisplayFinalProductAllJSON(request):
    pattern = request.GET['pattern']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid), (select P.productname from products P where P.productid = FP.productid) from finalproducts FP where finalproductname like '%{}%'".format(pattern)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)



def FinalProductSubmit(request):
    try:
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productid = request.POST['productid']
        finalproductname = request.POST['finalproductname']
        size = request.POST['size']
        sizeunit = request.POST['sizeunit']
        weight = request.POST['weight']
        weightunit = request.POST['weightunit']
        color = request.POST['color']
        price = request.POST['price']
        stock = request.POST['stock']

        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]

        q = "insert into finalproducts (categoryid, subcategoryid, productid, finalproductname, size, sizeunit, weight, weightunit, color, price, stock, picture) values ({}, {}, {}, '{}', '{}', '{}', {}, '{}', '{}', {}, {}, '{}' )".format(
            categoryid, subcategoryid, productid, finalproductname, size, sizeunit, weight, weightunit, color, price, stock, filename)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/MM/assets/"+filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        return render(request, "FinalProductInterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "FinalProductInterface.html", {'msg': 'Fail to Submit Record'})


def DisplayAllFinalProduct(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid), (select P.productname from products P where P.productid = FP.productid) from finalproducts FP"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayAllFinalProduct.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllFinalProduct.html", {'rows': []})


def DisplayFinalProductById(request):
    finalproductid = request.GET['finalproductid']
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = FP.subcategoryid), (select P.productname from products P where P.productid = FP.productid) from finalproducts FP where finalproductid = {}".format(finalproductid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return render(request, "DisplayFinalProductbyId.html", {'row': row})
    except Exception as e:
        print(e)
        return render(request, "DisplayFinalProductById.html", {'row': []})


def EditDeleteFinalProductRecord(request):
    btn = request.GET['btn']
    finalproductid = request.GET['finalproductid']
    if(btn == "Edit"):
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductname = request.GET['finalproductname']
        size = request.GET['size']
        sizeunit = request.GET['sizeunit']
        weight = request.GET['weight']
        weightunit = request.GET['weightunit']
        color = request.GET['color']
        price = request.GET['price']
        stock = request.GET['stock']
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "update finalproducts set categoryid = {}, subcategoryid = {}, productid = {}, finalproductname = '{}', size = '{}', sizeunit = '{}', weight = {}, weightunit = '{}', color = '{}', price = {}, stock = {} where finalproductid={}".format(
                categoryid, subcategoryid, productid, finalproductname, size, sizeunit, weight, weightunit, color, price, stock, finalproductid)
            print(q)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllFinalProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllFinalProduct(request)

    elif(btn == "Delete"):
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "delete from finalproducts where finalproductid={}".format(
                finalproductid)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllFinalProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllFinalProduct(request)


def EditFinalProductPicture(request):
    try:
        finalproductid = request.GET['finalproductid']
        finalproductname = request.GET['finalproductname']
        picture = request.GET['picture']
        row = [finalproductid, finalproductname, picture]
        return render(request, "EditFinalProductPicture.html", {'row': row})
    except Exception as e:
        return render(request, "EditFinalProductPicture.html", {'row': []})


def SaveEditFinalProductPicture(request):
    try:
        finalproductid1 = request.POST['finalproductid1']
        oldpicture = request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]

        q = "update finalproducts set picture = '{}' where finalproductid = {}".format(
            filename, finalproductid1)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        F = open("D:/MM/assets/"+filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        dbe.close()
        os.remove('D:/MM/assets/'+oldpicture)
        return DisplayAllFinalProduct(request)
    except Exception as e:
        print("Error :", e)
        return DisplayAllFinalProduct(request)


def GetFinalProductJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        productid = request.GET['productid']
        q = "select * from finalproducts where productid= {}".format(productid)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def DisplayFinalProductEmployee(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select FP.*,(select C.categoryname from categories C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = FP.subcategoryid), (select P.productname from products P where P.productid = FP.productid) from finalproducts FP"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayFinalProductEmployee.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayFinalProductEmployee.html", {'rows': []})
