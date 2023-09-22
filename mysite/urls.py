from django.urls import path
# from . import views
from mysite import trimDatabaseCsv

urlpatterns = [

	path('', trimDatabaseCsv.convert_database, name='coverter'),

	# path('', views.post_list, name='post_list'),
	# path('articles/', views.articles, name='articles'),
]
