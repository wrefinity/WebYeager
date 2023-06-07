from django.urls import path
from .views import world_list_view, world_featured,\
    world_delete_view, world_detail_view, world_instance_detail_view, \
    world_instance_delete_view, world_instance_list_view, tag_list_view,\
        tag_create_view, tag_detail_view, tag_delete_view, search_view, rate_world_view, world_navabr


app_name = "worlds"
urlpatterns = [
    path('list', world_list_view, name="world_list"),
    path('featured', world_featured, name="world_featured"),
    path('search', search_view, name='world_search'),
    path('nav_world', world_navabr, name='world_navabr'),
    
    path('detail/<str:slug>/', world_detail_view, name="world_detail"),
    path('delete/<str:slug>/', world_delete_view, name="world_delete"),
    path('rate/<str:slug>/', rate_world_view, name='world_rating'),

    # world instance
    path('instance/list', world_instance_list_view, name="world_instance_list"),
    path('instance/<str:slug>/', world_instance_detail_view, name="world_instance_detail"),
    path('instance/delete/<str:uuid>/', world_instance_delete_view, name="world_instance_delete"),

    # Tag urls Definitions
    path('tags', tag_list_view, name="tag_list"),
    path('tags/create', tag_create_view, name="tag_create"),
    path('tags/<int:id>/', tag_detail_view, name="tag_detail"),
    path('tags/delete/<int:id>/', tag_delete_view, name="tag_delete"),
]