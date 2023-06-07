from django.urls import path

from yeager_ai.users.views import user_detail_view, user_logout_view, \
    user_redirect_view, user_update_view, user_list_view, user_over_view
app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("logout/", view=user_logout_view, name="logout"),
    path("~update/", view=user_update_view, name="update"),
    path("detailss/", view=user_list_view, name="userx_detail"),
    path("overview/", view=user_over_view, name="users_overview"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
