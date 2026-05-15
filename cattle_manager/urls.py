from django.urls import path
from cattle_manager import views

urlpatterns = [
    path('',views.dashboard,name='cattle_dashboard'),
    path('cattles/',views.cattle_list,name='cattle_list'),
    path('cattle/<str:cattle_id>/',views.cattle_detail,name='cattle_detail'),
    path('add-cattle/',views.add_cattle,name='add_cattle'),
]