from django.urls import path, re_path

from . import views


urlpatterns = [
    path('pets/bear', views.BearPetListView.as_view()),
    path('pets', views.PetListView.as_view()),
    path('pets/<slug:pet_id>', views.PetView.as_view()),
    re_path(r'pets/(?P<category>dog|cat)',
            views.PetListOfCategoryView.as_view()),
]
