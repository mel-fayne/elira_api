from django.urls import path

from news.views import AllNewsPiecesView, NewsPieceByTagView

urlpatterns = [
    path('all_news', AllNewsPiecesView.as_view()),
    path('filter_news', NewsPieceByTagView.as_view())
]