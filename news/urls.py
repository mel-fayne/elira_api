from django.urls import path

from news.views import AllNewsPiecesView, NewsPiecesByTagView, AllTechEventsView, TechEventsByDateView, AllTechJobsView, TechJobsByAreaView

urlpatterns = [
    path('all_news', AllNewsPiecesView.as_view()),
    path('filter_news', NewsPiecesByTagView.as_view()),

    path('all_events', AllTechEventsView.as_view()),
    path('filter_events', TechEventsByDateView.as_view()),

    path('all_jobs', AllTechJobsView.as_view()),
    path('filter_jobs', TechJobsByAreaView.as_view()),
]
