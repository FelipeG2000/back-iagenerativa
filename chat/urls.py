from django.urls import path
from .views import Answer


urlpatterns = [
    path('answer/', Answer.as_view(), name='answer'),
]