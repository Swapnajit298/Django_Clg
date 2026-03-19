from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:id>/createdAt:<int:year>/<int:month>/<int:date>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment')
]
