from django.urls import path

from news.views import NewsPiecesByTagView, TechEventsByDateView, TechJobsByAreaView

urlpatterns = [
    path('filter_news/<int:student_id>', NewsPiecesByTagView.as_view()),
    path('filter_events/<int:period>', TechEventsByDateView.as_view()),
    path('filter_jobs/<int:student_id>', TechJobsByAreaView.as_view()),
]
