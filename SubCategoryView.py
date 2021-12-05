from django.shortcuts import render
from django.http import JsonResponse

from . import Pool
import uuid
import os
def SubCategoryInterface(request):
    return render(request,"SubcategoryInterface.html")

def GetSubcategoryJSON(request):
    try:
        db,cmd=Pool.ConnectionPool()
        categoryid=request.GET['categoryid']
        q="select * from subcategories where categoryid={}".format(categoryid)
        print(q)
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error',e)
        return JsonResponse(rows,safe=False)


def SubCategorySubmit(request):
    try:
        categoryid=request.POST['categoryid']
        subcategoryname=request.POST['subcategoryname']
        scdescription=request.POST['scdescription']
        icon=request.FILES['subcategoryicon']
        subcategoryicon=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into subcategories(categoryid,subcategoryname,scdescription,subcategoryicon)values({},'{}','{}','{}')".format(categoryid,subcategoryname,scdescription,subcategoryicon)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/"+subcategoryicon,"wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"SubcategoryInterface.html",{'msg':'Record submitted Successfully'})
    except Exception as e:
        print('error',e)
        return render(request,"SubcategoryInterface.html",{'msg':'Record submition failed'})

def DisplaySubCategories(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select * from subcategories"
        cmd.execute(q)
        rows=cmd.fetchall()
        return render(request,'DisplaySubcategories.html',{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,'DisplaySubcategories.html', {'rows':[]})

def DisplaySubcategoryById(request):
    subcategoryid=request.GET['subcategoryid']
    try:
        db, cmd = Pool.ConnectionPool()
        q = "select * from subcategories where subcategoryid={}".format(subcategoryid)
        cmd.execute(q)
        row = cmd.fetchone()
        return render(request,'DisplaySubcategoryById.html', {'row': row})
    except Exception as e:
        print('error', e)
        return render(request,'DisplaySubcategoryById.html', {'row': []})

def EditDeleteSubategory(request):
    btn=request.GET['btn']
    subcategoryid=request.GET["subcategoryid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        subcategoryname=request.GET['subcategoryname']
        scdescription=request.GET['scdescription']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "update subcategories set subcategoryname='{}' , scdescription='{}' where subcategoryid={}".format(subcategoryname,scdescription,subcategoryid)
            print (q)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplaySubCategories(request)
        except Exception as e:
            print("Error:", e)
            return DisplaySubCategories(request)

    elif (btn=="Delete"):

        try:
            db, cmd = Pool.ConnectionPool()
            q = "delete from subcategories where subcategoryid={}".format(subcategoryid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplaySubCategories(request)
        except Exception as e:
            print(e)
            return DisplaySubCategories(request)

def EditSubategoryIcon(request):
    try:
        subcategoryid=request.GET['subcategoryid']
        subcategoryname=request.GET['subcategoryname']
        subcategoryicon=request.GET['subcategoryicon']
        row=[subcategoryid,subcategoryname,subcategoryicon]
        return render(request,"EditSubcategoryIcon.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"EditSubcategoryIcon.html",{'row':[]})

def SaveEditSubcategoryIcon(request):
    try:
        subcategoryid=request.POST['subcategoryid']
        oldpicture=request.POST['oldicon']
        picture=request.FILES['subcategoryicon']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update subcategories set subcategoryicon='{}' where subcategoryid={}".format(filename,subcategoryid)
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
        return DisplaySubCategories(request)
    except Exception as e:
        print("Error:", e)
        return DisplaySubCategories(request)