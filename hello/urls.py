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
  # path('<int:id>/keyword_delete/<int:pk>', views.keyword_delete,
  # name="keyword_delete"),
  path('<int:id>/keyword_delete/<int:pk>', views.KeywordDeleteView.as_view(),
  name="keyword_delete"),
  path('<int:pk>/send_date/', views.SendDateView.as_view(),
  name="send_date"),
  path('<int:pk>/send_set/', views.SendSetView.as_view(),
  name="send_set"),
  path('<int:id>/send_change/<int:pk>/', views.SendChangeView.as_view(),
  name="send_change"),
  path('<int:id>/send_delete/<int:pk>/', views.SendDeleteView.as_view(),
  name="send_delete"),
]