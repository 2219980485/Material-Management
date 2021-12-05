from django.shortcuts import render
from . import Pool
from django.http import JsonResponse
import uuid
import os
def ProductInterface(request):
    return render(request,"ProductInterface.html")

def ProductSubmit(request):
    try:
        categoryid=request.POST['categoryid']
        subcategoryid=request.POST['subcategoryid']
        productname=request.POST['productname']
        pdescription=request.POST['pdescription']
        icon=request.FILES['producticon']
        producticon=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into products(categoryid,subcategoryid,productname,pdescription,icon)values({},{},'{}','{}','{}')".format(categoryid,subcategoryid,productname,pdescription,producticon)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/"+producticon,"wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"ProductInterface.html",{'msg':'Record submitted Successfully'})
    except Exception as e:
        print('error',e)
        return render(request,"ProductInterface.html",{'msg':'Record submition failed'})

def DisplayProducts(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q = "select P.*,(select C.categoryname from categories C where C.categoryid=P.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid=P.subcategoryid) from products P"
        cmd.execute(q)
        rows=cmd.fetchall()
        return render(request,'DisplayProducts.html',{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,'DisplayProducts.html', {'rows':[]})

def DisplayProductById(request):
    productid=request.GET['productid']
    try:
        db, cmd = Pool.ConnectionPool()
        q = "select * from products where productid={}".format(productid)
        cmd.execute(q)
        row = cmd.fetchone()
        return render(request,'DisplayProductById.html', {'row': row})
    except Exception as e:
        print('error', e)
        return render(request,'DisplayProductById.html', {'row': []})

def EditDeleteProduct(request):
    btn=request.GET['btn']
    productid=request.GET["productid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        categoryid=request.GET['categoryid']
        subcategoryid=request.GET['subcategoryid']
        productname=request.GET['productname']
        pdescription=request.GET['pdescription']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "update products set categoryid={},subcategoryid={},productname='{}' , pdescription='{}' where productid={}".format(categoryid,subcategoryid,productname,pdescription,productid)
            print (q)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayProducts(request)
        except Exception as e:
            print("Error:", e)
            return DisplayProducts(request)

    elif (btn=="Delete"):

        try:
            db, cmd = Pool.ConnectionPool()
            q = "delete from products where productid={}".format(productid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayProducts(request)
        except Exception as e:
            print(e)
            return DisplayProducts(request)

def EditProductIcon(request):
    try:
        productid=request.GET['productid']
        productname=request.GET['productname']
        producticon=request.GET['producticon']
        row=[productid,productname,producticon]
        return render(request,"EditProductIcon.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"EditProductIcon.html",{'row':[]})

def SaveEditProductIcon(request):
    try:
        productid=request.POST['productid']
        oldpicture=request.POST['oldicon']
        picture=request.FILES['icon']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update products set icon='{}' where productid={}".format(filename,productid)
        print(q)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('D:/MM/assets/'+oldpicture)
        return DisplayProducts(request)
    except Exception as e:
        print("Error:", e)
        return DisplayProducts(request)

def GetProductJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        subcategoryid = request.GET['subcategoryid']
        q = "select * from products where subcategoryid= {}".format(
            subcategoryid)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)
def DisplayProductEmployee(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select P.*,(select C.categoryname from categories C where C.categoryid = P.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = P.subcategoryid) from products P"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        result = request.session['EMPLOYEE']
        return render(request, "DisplayProductEmployee.html", {'rows': rows, 'result':result})
    except Exception as e:
        print(e)
        return render(request, "DisplayProductEmployee.html", {'rows': []})
