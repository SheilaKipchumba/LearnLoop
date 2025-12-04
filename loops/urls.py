from django.urls import path
from . import views

urlpatterns = [
    path('', views.loops_list, name='loops_list'),
    path('create/', views.create_loop, name='create_loop'),
    path('my-loops/', views.my_loops, name='my_loops'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('<int:pk>/', views.loop_detail, name='loop_detail'),
    path('<int:pk>/edit/', views.edit_loop, name='edit_loop'),
    path('<int:pk>/delete/', views.delete_loop, name='delete_loop'),
    path('<int:pk>/like/', views.like_loop, name='like_loop'),
]