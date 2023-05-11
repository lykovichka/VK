from django.urls import path

from .views import LoginView

urlpatterns = [
    path('account/', views.user_account, name = 'user_account'),
    path('account_setting/', views.account_setting, name = 'account_setting'),
    path('friends/', views.friends, name = 'friends'),
    path('friend_request/', views.friend_request, name = 'friend_request'),
    path('id<int:account_id>/add_friend', views.add_friend, name = 'add_friend'),

    path('confirm_friend<int:account_id>/', views.confirm_friend, name = 'confirm_friend'),
    path('delete_friend<int:account_id>/', views.delete_friend, name = 'delete_friend'),

    path('users/', views.find_users, name = 'find_users'),
    path('id<int:account_id>/', views.account, name = 'account'),
    ]