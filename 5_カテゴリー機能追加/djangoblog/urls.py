from django.urls import path
from .views import PostListView,PostDetailView,PostListByCategoryView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostListByCategoryView.as_view(), name='post_list_by_category'),
]