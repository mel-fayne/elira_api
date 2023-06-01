from django.urls import path

from progress.views import AllProjectIdeasView, AppDataView, ProjectIdeasView, StudentIdeaWishListView, StudentProjectView


urlpatterns = [
    path('todays_ideas/<str:specialisation>', ProjectIdeasView.as_view()),
    path('project_ideas', ProjectIdeasView.as_view()),
    path('all_project_ideas', AllProjectIdeasView.as_view()),
    path('idea_wishlist/<int:student_id>', StudentIdeaWishListView.as_view()),
    path('student_projects/<int:student_id>', StudentProjectView.as_view()),
    path('student_project', StudentProjectView.as_view()),
    path('student_project/<int:project_id>', StudentProjectView.as_view()),

    path('app_data', AppDataView.as_view()),
]