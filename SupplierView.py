from django.shortcuts import render
from django.http import JsonResponse
from . import Pool


def SupplierInterface(request):
    try:
        result = request.session['ADMIN']
        return render(request, "SupplierInterface.html")
    except Exception as e:
        return render(request, 'AdminLogin.html')


def SupplierSubmit(request):
    try:
        suppliername = request.GET['suppliername']
        landlinenumber = request.GET['landlinenumber']
        mobilenumber = request.GET['mobilenumber']
        emailid = request.GET['emailid']
        address = request.GET['address']
        state = request.GET['state']
        city = request.GET['city']

        q = "insert into supplier (suppliername, landlinenumber, mobilenumber, emailid, address, stateid, cityid) values ('{}', '{}', '{}', '{}', '{}', {}, {})".format(
            suppliername, landlinenumber, mobilenumber, emailid, address, state, city)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return render(request, "SupplierInterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "SupplierInterface.html", {'msg': 'Fail to Submit Record'})


def DisplayAllSupplier(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select SR.*,(select C.cityname from Cities C where C.cityid = SR.cityid), (select S.statename from States S where S.stateid = SR.stateid) from supplier SR"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayAllSupplier.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllSupplier.html", {'rows': []})


def GetSupplierJSON(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select * from supplier"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(rows, safe=False)
