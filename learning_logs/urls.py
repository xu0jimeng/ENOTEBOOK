"""定义 learning_logs的url模式"""

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
	# index
	path('', views.index, name= 'index'),
	path('topics/', views.topics, name = 'topics'),
	path('topics/<int:topic_id>/', views.topic, name = 'topic'),
	path('new_topic/', views.new_topic, name = 'new_topic'),
	path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),
	path('edit_entry/<int:entry_id>/', views.edit_entry, name = 'edit_entry'),
	path('items/', views.items, name = 'items'),
]

app_name = 'learning_logs'
"""如果没有app_name 则会报错：learning_logs' is not a registered namespace"""