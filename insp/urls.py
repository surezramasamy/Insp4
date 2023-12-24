from django.urls import path
from django.urls import path
from .views import part_group,part_list, part_detail,upload_drawings
from . import views

urlpatterns = [
    
    path('part_list/<int:pk>/', part_list, name='part_list'),\
    path('', part_group, name='part_group'),
    path('<int:pk>/', part_detail, name='part_detail'),
    path('Insp', views.Insp_view, name='Insp'), 
    path('input_num_extra_forms/', views.input_num_extra_forms, name='input_num_extra_forms'),
    path('upload_drawings/<int:num_extra_forms>/', views.upload_drawings, name='upload_drawings')
   
]