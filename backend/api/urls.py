from django.urls import path
from .views import set_domains, get_domains


urlpatterns = [
    path('visited_links/', set_domains, name='set_domains'),
    path('visited_domains', get_domains, name='get_domains')
]
