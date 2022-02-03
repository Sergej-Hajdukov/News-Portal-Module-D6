from django.urls import path
from .views import NewsList, NewsDetail, SearchNews, AddNews, DeleteNews, UpdateNews, add_subscribe, \
    del_subscribe


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', SearchNews.as_view(), name='news_search'),
    path('add/', AddNews.as_view(), name='news_add'),
    path('<int:pk>/edit/', UpdateNews.as_view(), name='news_update'),
    path('<int:pk>/delete/', DeleteNews.as_view(), name='news_delete'),
    path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]
