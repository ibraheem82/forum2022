from django.urls import path
from . import views

"""
    ===> if a user goes to [/api] it will display the home [api]
"""
urlpatterns = [

    
    
    
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
    
    
]