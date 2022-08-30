from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

#app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<str:cat>', views.post_list, name='post_cat'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_details, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name="post_share")
]
