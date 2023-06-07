from django.urls import path
from .views import agent_navbar, agents_create_view, rate_agent_view, agent_delete_view, agents_list_view, agents_detail_view, api_my__agent_view, agents_tab_view

app_name = "agents"
urlpatterns = [
    path('list', agents_list_view, name="agent_list"),
    path('tab', agents_tab_view, name="agent_tab"),
    path('create', agents_create_view, name="agent_create"),
    path('<slug:slug>/', agents_detail_view, name="agent_detail"),
    path('delete/<slug:slug>/', agent_delete_view, name="agent_delete"),
    path('rate/<str:slug>/', rate_agent_view, name='agent_rating'),
    path('me', api_my__agent_view, name="agent_user"),
    path('nav_agent', agent_navbar, name="agent_navbar"),
   
]
