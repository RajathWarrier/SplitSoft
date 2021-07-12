from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view()),
    path('logout/', views.logoutView),
    path('register/', views.registration_view),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('newgroup/', views.newgroupview, name='newgroupview'),
    path('group/<int:id>', views.groupview, name='groupview'),
    path('group/<int:g_id>/add', views.adduserview, name='adduserview'),
    path('group/<int:g_id>/add/<int:u_id>', views.adduserconfirmation, name='adduserconfirmation'),
    path('group/<int:g_id>/remove/<int:u_id>', views.removeuserview, name='removeuserview'),
    path('group/<int:g_id>/addexpense', views.addexpenseview, name='addexpenseview'),
    path('group/<int:g_id>/expenses', views.expensesview, name='expensesview'),
    path('group/<int:g_id>/deleteexpense/<int:e_id>', views.deleteexpenseview, name='deleteexpenseview'),
    path('group/<int:g_id>/split', views.showsplitview, name='showsplitview'),
    path('group/<int:g_id>/settle/<int:s_id>', views.settleview, name='settleview'),
    path('group/chat/<str:room_name>', views.chatroom, name='chatroom')
]