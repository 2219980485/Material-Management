from django.shortcuts import render
from . import PoolDict


def AdminLogout(request):
   del request.session['ADMIN']
   return render(request,'AdminLogin.html')

def AdminLogin(request):
    try:
     result=request.session['ADMIN']
     return render(request, "AdminDashBoard.html", {'result': result})

    except Exception as e:

     return render(request,'AdminLogin.html')
def CheckAdminLogin(request):
    try:
     emailid=request.POST['emailid']
     password = request.POST['password']

     db, cmd = PoolDict.ConnectionPool()
     q="select * from admins where emailid='{}' and password='{}'".format(emailid,password)
     cmd.execute(q)
     result=cmd.fetchone()
     print(result)
     if(result):
         request.session['ADMIN']=result
         return render(request, "AdminDashBoard.html", {'result': result})
     else:
         return render(request, "AdminLogin.html", {'result': result,'msg':"Invalid Emailid/Password"})
     db.close()

    except Exception as e:
      print (e)
      return render(request, "AdminLogin.html", {'result': {},'msg':'Server Error'})