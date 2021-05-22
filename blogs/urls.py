from django.urls import path
from blogs import views

urlpatterns = [path("articles", views.ListCreatePostAPIView.as_view(), name="articles")]
