from django.urls import path

from app.views import MainPageView
app_name = 'app'

urlpatterns = [
    path('', MainPageView.as_view(), name='index')
]