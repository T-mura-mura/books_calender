from django.urls import path
from . import views

app_name = 'hello'
urlpatterns = [
  path('', views.BooksListView.as_view(), name="index"),
  path('<int:pk>/keyword_list/', views.KeywordsListView.as_view(),
  name="keyword_list"),
  path('<int:pk>/keyword_add/', views.KeywordAddView.as_view(),
  name="keyword_add"),
  path('<int:id>/keyword_edit/<int:pk>/', views.KeywordEditView.as_view(),
  name="keyword_edit"),
  path('keyword/ajax_delete/', views.keyword_ajax_delete, 
  name="keyword_ajax_delete"),
  path('<int:pk>/send_date/', views.SendDateView.as_view(),
  name="send_date"),
  path('<int:pk>/send_set/', views.SendSetView.as_view(),
  name="send_set"),
  path('<int:id>/send_change/<int:pk>/', views.SendChangeView.as_view(),
  name="send_change"),
  path('<int:id>/send_delete/<int:pk>/', views.SendDeleteView.as_view(),
  name="send_delete"),
  path('<int:pk>/email_list/', views.EmailListView.as_view(),
  name="email_list"),
  path('<int:id>/email_edit/<int:pk>/', views.EmailEditView.as_view(),
  name="email_edit"),
]