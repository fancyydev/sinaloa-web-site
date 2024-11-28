from django.urls import path
from .views import *

app_name = 'restaurant_branches' 
urlpatterns = [
    path('ask-openai/', ask_openai, name='ask_openai'),
    path('ask-gemini/', ask_gemini, name='ask_gemini'),
    path('handle_user_query/', handle_user_query, name='handle_user_query'),
]
