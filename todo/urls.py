from django.urls import path
from .views import *

urlpatterns=[
    path('', Home.as_view(), name="home"),
    path('project/<int:pk>',ProjectDetailView.as_view(), name="detail-project"),
    path('project/add', ProjectCreateView.as_view() ,name="create-project"),
    path('project/update/<int:pk>', ProjectUpdateView.as_view(), name="update-project"),
]