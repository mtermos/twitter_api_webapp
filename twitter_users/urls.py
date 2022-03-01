from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login_page/', views.login_page, name="login_page"),
    path('twitter_login/', views.twitter_rm_rt_login, name='twitter_rm_rt_login'),
    path('twitter_login_dm/', views.twitter_dm_login, name='twitter_dm_login'),
    path('twitter_rm_rt/twitter_callback/', views.twitter_rm_rt_callback, name='twitter_rm_rt_callback'),
    path('twitter_dm/twitter_callback/', views.twitter_dm_callback, name='twitter_dm_callback'),
    path('twitter_logout/', views.twitter_logout, name='twitter_logout'),

    path('remove_retweets/create_page', views.remove_retweets_create_page, name='remove_retweets_create_page'),
    path('remove_retweets/create', views.remove_retweets_create, name='remove_retweets_create'),

    path('welcome_message/create_page', views.welcome_message_create_page, name='welcome_message_create_page'),
    path('welcome_message/create', views.welcome_message_create, name='welcome_message_create'),
    path('welcome_message/delete/<str:id>', views.welcome_message_delete, name='welcome_message_delete'),
    path('welcome_message/make_default', views.make_welcome_message_default, name='make_welcome_message_default'),
    path('welcome_message/edit/<str:id>', views.welcome_message_edit, name='welcome_message_edit'),
    path('welcome_message/update', views.welcome_message_update, name='welcome_message_update'),

    path('auto_retweet/create', views.auto_retweet_create, name='auto_retweet_create'),
    path('auto_retweet/store', views.auto_retweet_store, name='auto_retweet_store'),
]