from django.urls import path
from scraper.views import *

urlpatterns = [
    path('receive-data', receive_data, name='receive_data'),
    path('', show_data, name='get_data'),
    path('test', test, name='test'),
]
