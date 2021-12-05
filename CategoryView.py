from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import uuid
import os

def CategoryInterface(request):
    return render(request,"CategoryInterface.html")

def CategorySubmit(request):
    try:
        categoryname=request.POST['categoryname']
        icon=request.FILES['categoryicon']
        categoryicon=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into categories(categoryname,categoryicon)values('{}','{}')".format(categoryname,categoryicon)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/"+categoryicon,"wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"CategoryInterface.html",{'msg':'Record submitted Successfully'})
    except Exception as e:
        print('error',e)
        return render(request,"CategoryInterface.html",{'msg':'Record submition failed'})

def DisplayCategories(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select * from categories"
        cmd.execute(q)
        rows=cmd.fetchall()
        return render(request,'DisplayCategories.html',{'rows':rows})
    except Exception as e:
        print('error',e)
        return render(request,'DisplayCategories.html', {'rows':[]})


def GetCategoriesJSON(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select * from categories"
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print('error',e)
        return JsonResponse([], safe=False)




def DisplayCategoryById(request):
    categoryid=request.GET['categoryid']
    try:
        db, cmd = Pool.ConnectionPool()
        q = "select * from categories where categoryid={}".format(categoryid)
        cmd.execute(q)
        row = cmd.fetchone()
        return render(request,'DisplayCategoryById.html', {'row': row})
    except Exception as e:
        print('error', e)
        return render(request,'DisplayCategoryById.html', {'row': []})

def EditDeleteCategory(request):
    btn=request.GET['btn']
    categoryid=request.GET["categoryid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        categoryname=request.GET['categoryname']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "update categories set categoryname='{}' where categoryid={}".format(categoryname,categoryid)
            print (q)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayCategories(request)
        except Exception as e:
            print("Error:", e)
            return DisplayCategories(request)

    elif (btn=="Delete"):

        try:
            db, cmd = Pool.ConnectionPool()
            q = "delete from categories where categoryid={}".format(categoryid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayCategories(request)
        except Exception as e:
            print(e)
            return DisplayCategories(request)

def EditCategoryIcon(request):
    try:
        categoryid=request.GET['categoryid']
        categoryname=request.GET['categoryname']
        categoryicon=request.GET['categoryicon']
        row=[categoryid,categoryname,categoryicon]
        return render(request,"EditCategoryIcon.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"EditCategoryIcon.html",{'row':[]})

def SaveEditCategoryIcon(request):
    try:
        categoryid=request.POST['categoryid']
        oldpicture=request.POST['oldicon']
        picture=request.FILES['categoryicon']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update categories set categoryicon='{}' where categoryid={}".format(filename,categoryid)
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
        return DisplayCategories(request)
    except Exception as e:
        print("Error:", e)
        return DisplayCategories(request)