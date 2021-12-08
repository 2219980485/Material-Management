"""MM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import EmployeeView
from . import StateCityView

from . import CategoryView
from . import SubCategoryView
from . import ProductView
from . import AdminView
from . import FinalProductView
from . import SupplierView
from . import PurchaseView
from . import IssueView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogin/',AdminView.AdminLogin),
    path('checkadminlogin',AdminView.CheckAdminLogin),
    path('adminlogout/', AdminView.AdminLogout),
    # Employee Urls
    path('employeelogin/',EmployeeView.EmployeeLogin),
    path('employeedashboard/',EmployeeView.EmployeeDashboard),
    path('checkemployeelogin',EmployeeView.CheckEmployeeLogin),
    path('employeelogout/',EmployeeView.EmployeeLogout),
    #Employee
    path('employeeinterface/',EmployeeView.EmployeeInterface),
    path('employeesubmit',EmployeeView.EmployeeSubmit),
    path('displayall/',EmployeeView.DisplayAll),
    path('displayemployeebyid/', EmployeeView.DisplayById),
    path('editdeleterecord/', EmployeeView.EditDeleteRecord),
    path('editemployeepicture/', EmployeeView.EditEmployeePicture),
    path('saveeditpicture', EmployeeView.SaveEditPicture),



    path('fetchallstates/', StateCityView.FetchAllStates),
    path('fetchallcities/', StateCityView.FetchAllCities),
    #Category
    path('categoryinterface/',CategoryView.CategoryInterface),
    path('categorysubmit',CategoryView.CategorySubmit),
    path('displaycategories/',CategoryView.DisplayCategories),
    path('getcategoriesjson',CategoryView.GetCategoriesJSON),
    path('displaycategorybyid/',CategoryView.DisplayCategoryById),
    path('editdeletecategory/',CategoryView.EditDeleteCategory),
    path('editcategoryicon/',CategoryView.EditCategoryIcon),
    path('saveeditcategoryicon',CategoryView.SaveEditCategoryIcon),
    #subcategory
    path('subcategoryinterface/',SubCategoryView.SubCategoryInterface),
    path('subcategorysubmit',SubCategoryView.SubCategorySubmit),
    path('displaysubcategories/',SubCategoryView.DisplaySubCategories),
    path('displaysubcategorybyid/',SubCategoryView.DisplaySubcategoryById),
    path('editdeletesubcategory/',SubCategoryView.EditDeleteSubategory),
    path('editsubcategoryicon/',SubCategoryView.EditSubategoryIcon),
    path('saveeditsubcategoryicon',SubCategoryView.SaveEditSubcategoryIcon),
    path('getsubcategoryjson/',SubCategoryView.GetSubcategoryJSON),
  #Product
       path('productinterface/',ProductView.ProductInterface),
       path('productsubmit',ProductView.ProductSubmit),
       path('displayproducts/',ProductView.DisplayProducts),
       path('displayproductbyid/',ProductView.DisplayProductById),
       path('editdeleteproduct/',ProductView.EditDeleteProduct),
       path('editproducticon/',ProductView.EditProductIcon),
       path('getproductjson/', ProductView.GetProductJSON),
       path('saveeditproducticon',ProductView.SaveEditProductIcon),
       path('displayproductemployee/',ProductView.DisplayProductEmployee),

# FinalProduct Urls
    path('finalproductinterface/',FinalProductView.FinalProductInterface),
    path('finalproductsubmit',FinalProductView.FinalProductSubmit),
    path('displayallfinalproduct/',FinalProductView.DisplayAllFinalProduct),
    path('displayfinalproductbyid/',FinalProductView.DisplayFinalProductById),
    path('editdeletefinalproductrecord/',FinalProductView.EditDeleteFinalProductRecord),
    path('editfinalproductpicture/',FinalProductView.EditFinalProductPicture),
    path('saveeditfinalproductpicture',FinalProductView.SaveEditFinalProductPicture),
    path('getfinalproductjson/',FinalProductView.GetFinalProductJSON),
    path('displayfinalproductemployee/',FinalProductView.DisplayFinalProductEmployee),
    path('displayfinalproductbyidjson/',FinalProductView.DisplayFinalProductByIdJSON),
    path('displayfinalproductalljson/',FinalProductView.DisplayFinalProductAllJSON),
    path('displayupdatedstock/',FinalProductView.DisplayUpdatedStock),
# Supplier Urls
    path('supplierinterface/',SupplierView.SupplierInterface),
    path('suppliersubmit/',SupplierView.SupplierSubmit),
    path('displayallsupplier/',SupplierView.DisplayAllSupplier),
    path('getsupplierjson/',SupplierView.GetSupplierJSON),

    # Purchase Urls
    path('purchaseinterface/', PurchaseView.PurchaseInterface),
    path('purchaseproductsubmit', PurchaseView.PurchaseProductSubmit),
    path('displayallpurchaseproduct/', PurchaseView.DisplayAllPurchaseProduct),
    path('editdeletepurchaseproductrecord/', PurchaseView.EditDeletePurchaseProductRecord),
    path('displaypuchasealljson/',PurchaseView.DisplayPurchaseAllJSON),
    path('listpurchaseemployee/',PurchaseView.ListPurchaseEmployee),

    # Issue Urls
    path('issueinterface/', IssueView.IssueInterface),
    path('issueproductsubmit', IssueView.IssueProductSubmit),
    path('displayallissueproduct/', IssueView.DisplayAllIssueProduct),
    path('editdeleteissueproductrecord/', IssueView.EditDeleteIssueProductRecord),
    path('displayissuealljson/',IssueView.DisplayIssueAllJSON),
    path('listissueemployee/',IssueView.ListIssueEmployee),
    
    
]
