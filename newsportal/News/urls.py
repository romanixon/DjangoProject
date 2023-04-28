from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(ViewNews.as_view()), name='home'),
    path('news/', cache_page(60 * 5)(ViewNews.as_view()), name='news'),
    path('news/<int:pk>', cache_page(60 * 5)(OneViewNews.as_view()), name='news_detail'),
    path('search/', cache_page(60 * 5)(SearchView.as_view()), name='search'),
    path('news/create', NewCreate.as_view(), name='new_create'),
    path('articles/create', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit', NewEdit.as_view(), name='new_edit'),
    path('articles/<int:pk>/edit', ArticleEdit.as_view(), name='article_edit'),
    path('news/<int:pk>/delete', NewDelete.as_view(), name='new_delete'),
    path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', cache_page(60 * 5)(CategoryListView.as_view()), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

]
