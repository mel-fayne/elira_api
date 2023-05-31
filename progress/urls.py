from django.urls import path

from progress.views import AllProjectIdeasView, AppDataView, ProjectIdeasView


urlpatterns = [
    path('todays_ideas/<str:specialisation>', ProjectIdeasView.as_view()),
    path('project_ideas', ProjectIdeasView.as_view()),
    path('all_project_ideas', AllProjectIdeasView.as_view()),

    path('app_data', AppDataView.as_view()),
]