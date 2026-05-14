from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.NoteShareLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.group_list, name='group_list'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('subgroup/<int:subgroup_id>/upload/', views.upload_note, name='upload_note'),
    path('<int:group_id>/create-subgroup/', views.create_subgroup, name='create_subgroup'),
]
