from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.LoginPage,name='login'),
    path('register/',views.RegisterPage,name='register'),
    path("activate/<uidb64>/<token>/", views.Activate, name="activate"),
    path('logout/',views.LogoutPage,name='logout'),
    path('profile/<str:pk>',views.userProfile,name='profile'),
    path('room/<str:pk>',views.room,name="room"),
    path('create_room/',views.createRoom,name="create-room"),
    path('update_room/<str:pk>',views.updateRoom,name="update-room"),
    path('delete_room/<str:pk>',views.deleteRoom,name="delete-room"),
    path('delete_message/<str:pk>',views.deleteMessage,name="delete-message"),
    path('update_user/',views.updateUser,name="update-user"),
    path('topic/',views.topicView,name="topic"),
    path('activity/',views.activityView,name="activity"),






]