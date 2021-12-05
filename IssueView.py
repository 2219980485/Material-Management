from django.shortcuts import render
from . import Pool


def IssueInterface(request):
    try:
        result = request.session['EMPLOYEE']
        print(result)
        return render(request, "IssueInterface.html",{'result':result})
    except Exception as e:
        return render(request, 'EmployeeLogin.html')


def IssueProductSubmit(request):
    try:
        employeeid = request.POST['employeeid']
        categoryid = request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productid = request.POST['productid']
        finalproductid = request.POST['finalproductid']
        demand_employeeid = request.POST['demand_employeeid']
        dateissue = request.POST['dateissue']
        qtyissue = request.POST['qtyissue']
        remark = request.POST['remark']

        q = "insert into issue (employeeid, categoryid, subcategoryid, productid, finalproductid, demand_employeeid, dateissue, qtyissue, remark) values ({}, {}, {}, {}, {}, {}, '{}', {}, '{}' )".format(
             employeeid, categoryid, subcategoryid, productid, finalproductid, demand_employeeid, dateissue, qtyissue, remark)
        print(q)
        dbe, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        # Update Stock

        q = "update finalproducts set  stock=stock-{} where finalproductid={}".format(qtyissue,finalproductid)
        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return render(request, "IssueInterface.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print("Error :", e)
        return render(request, "IssueInterface.html", {'msg': 'Fail to Submit Record'})

def DisplayAllIssueProduct(request):
    try:
        dbe, cmd = Pool.ConnectionPool()
        q = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid),(select S.subcategoryname from subcategories S where S.subcategoryid = IP.subcategoryid), (select P.productname from products P where P.productid = IP.productid), (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) from issue IP"
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return render(request, "DisplayAllIssueProduct.html", {'rows': rows})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllIssueProduct.html", {'rows': []})

def EditDeleteIssueProductRecord(request):
    btn = request.GET['btn']
    issueid = request.GET['issueid']
    if(btn == "Edit"):
        employeeid = request.GET['employeeid']
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        demand_employeeid = request.GET['demand_employeeid']
        dateissue = request.GET['dateissue']
        qtyissue = request.GET['qtyissue']
        remark = request.GET['remark']
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "update issue set employeeid = {}, categoryid = {}, subcategoryid = {}, productid = {}, finalproductid = {}, demand_employeeid = {}, dateissue = '{}', qtyissue = {}, remark = '{}' where issueid={}".format(
                employeeid, categoryid, subcategoryid, productid, finalproductid, demand_employeeid ,dateissue, qtyissue, remark, issueid)
            print(q)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllIssueProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllIssueProduct(request)

    elif(btn == "Delete"):
        try:
            dbe, cmd = Pool.ConnectionPool()
            q = "delete from issue where issueid={}".format(
                issueid)
            cmd.execute(q)
            dbe.commit()
            row = cmd.fetchone()
            dbe.close()
            return DisplayAllIssueProduct(request)
        except Exception as e:
            print(e)
            return DisplayAllIssueProduct(request)

def DisplayIssueAllJSON(request):
    fromdate = request.GET['fromdate']
    todate = request.GET['todate']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        # q = "select PP.*,(select C.categoryname from categories C where C.categoryid = PP.categoryid) as categoryname,(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid) as subcategoryname, (select P.productname from products P where P.productid = PP.productid) as productname, (select FP.finalproductname from finalproducts FP where FP.finalproductid = PP.finalproductid) as finalproductname, (select S.suppliername from supplier S where S.supplierid = PP.supplierid) as suppliername from purchase PP where datepurchase between '{}' and '{}'".format(fromdate,todate)
        q = "select IP.*,(select C.categoryname from categories C where C.categoryid = IP.categoryid) as categoryname,(select S.subcategoryname from subcategories S where S.subcategoryid = IP.subcategoryid) as subcategoryname, (select P.productname from products P where P.productid = IP.productid) as productname, (select FP.finalproductname from finalproducts FP where FP.finalproductid = IP.finalproductid) as finalproductname, (select E.firstname from employee E where E.employeeid = IP.demand_employeeid) as dfname, (select E.lastname from employee E where E.employeeid = IP.demand_employeeid) as flname,(select E.firstname from employee E where E.employeeid = IP.employeeid) as fname, (select E.lastname from employee E where E.employeeid = IP.employeeid) as lname from issue IP where dateissue between '{}' and '{}'".format(fromdate,todate)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def ListIssueEmployee(request):
    try:
        result = request.session['EMPLOYEE']
        return render(request,"ListIssueEmployee.html",{'result':result})
    except Exception as e:
        return render(request, 'EmployeeLogin.html')
